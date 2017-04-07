# we ran this programm in anaconda python compiler and imported some things that would have been needed to be installed
# for running it with the virtual machines

from flask import Flask, request

import time
import json
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict
import math

import user_user_collaborative
import response_handling
import item_item_collaborative


app = Flask(__name__)
user_item = {}
item_user = {}
item_count = {}
item_timer = {}
test_list1 = []
test_list2 = []
test_list3 = []
test_time = []

@app.route('/')
def index():
    return 'Index'

@app.route('/HELLO', methods=['POST'])
def hello():
    return 'READY'

@app.route('/TRAIN', methods=['POST'])
def train():
    # The template skips this phase; replace this code if you want Idomaar to control training of your model
    time.sleep(1)
    return 'OK\nhttp://192.168.22.100:5001'

@app.route('/TEST', methods=['POST'])
def test():
    return 'OK'

@app.route('/STOP', methods=['POST'])
def stop():
    print (user_item)
    return 'OK'


@app.route('/', methods=['POST'])
def recommend():

    #receiving and extracting  data
    recBody = json.loads(request.form.getlist('body')[0])
    recType = request.form.getlist('type')[0]

    # initialization for collaborative filtering
    user_user_result = [0]
    item_item_result = [0]

    #extract information of each recommendation request or event notification (they have the same struture)
    if (recType!="item_update"):
        try:
            userID = recBody['context']['simple']['57'] #might be 0 as well ;)
        except:
            userID = 0

        try:
            itemID = recBody['context']['simple']['25'] #might be 0!
        except:
            itemID = 0

        try:
            publisherID = recBody['context']['simple']['27']
        except:
            publisherID = 0

        #saves for each publisher which user read which articles
        user_item.setdefault(publisherID, defaultdict(list))
        user_item[publisherID][userID].append(itemID)

        # saves for each publisher which item was read by which userpl
        item_user.setdefault(publisherID, defaultdict(list))
        if itemID != 0:
            item_user[publisherID][itemID].append(userID)

    #extract information of each item_update
    else:
        publisherID = recBody['domainid']
        itemID = recBody['id']

    currentTime = recBody['timestamp']


    #counts for each publisher how often item was "touched" (in event_notification, recommendation_request or item_update)
    item_count.setdefault(publisherID, defaultdict())
    item_timer.setdefault(publisherID, defaultdict()) #set 1 for new item

    if itemID != 0:
        item_count[publisherID].setdefault(itemID, 0)
        item_count[publisherID][itemID] = item_count[publisherID][itemID] + 1
        item_timer[publisherID][itemID] = currentTime

    factor = 50
    norm_fromMiliToHours = 1000 * 60 * 60
    for key in item_count[publisherID].keys():
        timeSinceLastClick = currentTime - item_timer[publisherID][key]
        item_count[publisherID][key] *= -(math.pow((timeSinceLastClick * factor)/norm_fromMiliToHours, 2)) + 1
        if(item_count[publisherID][key] < 0):
            item_count[publisherID][key] = 0

    # save some information to plot test data
    # if publisherID == 35774:
    #      try:
    #          test_list1.append(item_count[35774][246519047])
    #      except:
    #          test_list1.append(0)
    #      try:
    #          test_list2.append(item_count[35774][257712455])
    #      except:
    #          test_list2.append(0)
    #      try:
    #          test_list3.append(item_count[35774][257643506])
    #      except:
    #          test_list3.append(0)
    #      test_time.append(currentTime)


    try:
        mostPopularItems = sorted(item_count[publisherID], key=item_count[publisherID].get, reverse=True)
    except:
        mostPopularItems = []

    ############################
    #building the rec-response
    ############################

    if (recType=="recommendation_request"):

        # get max 6 items from user_user collaborative filtering
        # (if userID = 0 he is treated as if he had only read the current item)
        if not ((userID == 0) or (itemID == 0)):
            user_user_result = user_user_collaborative.filtering(user_item[publisherID], userID)

        # get the 6 most similar items
        if not(itemID == 0):
            item_item_result = item_item_collaborative.filtering(item_user[publisherID], itemID, userID, user_item[publisherID])

        # get the limit of how many items to recommend
        limit = recBody['limit']
        # choose the version of the response_handling -> how different results should be combined
        version = 1

        resp = response_handling.output(version, limit, itemID, userID, mostPopularItems, user_user_result, item_item_result)

    print(resp)

    return app.make_response(json.dumps(resp))


if __name__ == '__main__':
    handler = RotatingFileHandler('http_flask_server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000)