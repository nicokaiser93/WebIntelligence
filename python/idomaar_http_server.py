from flask import Flask, request

import time
import json
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict

import user_user_collaborative
import response_handling
import item_item_collaborative

app = Flask(__name__)
user_item = {}
item_user = {}
item_count = {}

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

    #TODO ACHTUNG ACHTUNG!! BITTE FOLGENDES BEACHTEN:
    # habe 3 python files erstellt die am anfang importiert werden und damit etwas ausgelagert und versucht damit den
    # Überblick zu behalten
    # response_handling: bekommt alle Ergebnisse und man kann anhand der version entscheiden wie diese zu der resp
    # kombiniert werden
    # user_user_collaborative: der Name ist Programm --> gibt maximal 6 Artikel des ähnlichsten Users zurück
    # item_item_collaborative: der Name ist Programm --> gibt die 6 ähnlichstens Items zurück

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

        # saves for each publisher which item was read by which user
        item_user.setdefault(publisherID, defaultdict(list))
        if itemID != 0:
            item_user[publisherID][itemID].append(userID)

    #extract information of each item_update
    else:
        publisherID = recBody['domainid']
        itemID = recBody['id']


    #counts for each publisher how often item was "touched" (in event_notification, recommendation_request or item_update)
    item_count.setdefault(publisherID, defaultdict())
    if itemID != 0:
        item_count[publisherID].setdefault(itemID, 0)
        item_count[publisherID][itemID] = item_count[publisherID][itemID]+1

    #returns sorted list of which items were most often touched
    try:
        mostPopularItems = sorted(item_count[publisherID], key=item_count[publisherID].get)
    except:
        mostPopularItems = []


    ############################
    #building the rec-response
    ############################

    ### thoughts: ###
    # - time-dependant change of the response handling -> for example in the beginning user_user is useless but after
    #   a lot of requests it could be useful
    # - base everything on the mostPopularItems and connect the other two methods to a rating
    #   --> for example an item that is in the top 10 of popularity AND top 6 of similarity could lead to better results
    #       than an item that is "only" most popular or most similar
    # - it is maybe not optimal to compute all the results from most_popular, user_user and item_item although we may
    #   not use all of them in the response handling -> maybe call functions from the response handling
    # - testing has to done --> by now i have no idea how to combine the results best although item_item seems to have
    #   the most clicks for the small data set

    if (recType=="recommendation_request"):

        # get max 6 items from user_user collaborative filtering
        # (if userID = 0 he is treated as if he had only read the current item)
        if not ((userID == 0) and (itemID == 0)):
            user_user_result = user_user_collaborative.filtering(user_item[publisherID], userID, itemID)

        # get the 6 most similar items
        if not(itemID == 0):
            item_item_result = item_item_collaborative.filtering(item_user[publisherID], itemID)

        # get the limit of how many items to recommend
        limit = recBody['limit']
        # choose the version of the response_handling -> how different results should be combined
        version = 4
        resp = response_handling.output(version, limit, mostPopularItems, user_user_result, item_item_result)

    print(resp)

    return app.make_response(json.dumps(resp))


if __name__ == '__main__':
    handler = RotatingFileHandler('http_flask_server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000)