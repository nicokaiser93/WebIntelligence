from flask import Flask, request

import time
import json
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict
import numpy as np

app = Flask(__name__)
user_item = {}
item_count = {}
itemList = {}
itemArray = {}
itemArray_tmp = {}
userList = {}
global matrix
matrix = {}

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

def itemItem(user_item_publisher, userID):

    sim = {}
    for key in user_item_publisher.keys():
        if (key == userID) or (key == 0) or (userID == 0):
            sim[key] = 0
            continue
        this_user = user_item_publisher[userID]
        comp_user = user_item_publisher[key]
        sim.setdefault(key, 0)
        for i in this_user:
            if i in comp_user:
                sim[key] = sim[key] + 1

    most_similar_user = max(sim, key=sim.get)
    most_similar_item_list = user_item_publisher[most_similar_user]
    not_read_list = set(user_item_publisher[userID]) - set(most_similar_item_list)
    try:
        return not_read_list[0]
    except:
        return 0

@app.route('/', methods=['POST'])
def recommend():



    #receiving and extracting  data
    recBody = json.loads(request.form.getlist('body')[0])
    recType = request.form.getlist('type')[0]

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

        #print(recType+" user:"+str(userID)+" item:"+str(itemID)+" publisher:"+str(publisherID))

        #saves for each publisher which user read which articles
        user_item.setdefault(publisherID, defaultdict(list))
        #if itemID != 0:
            #user_item[publisherID][userID].append(itemID)
        user_item[publisherID][userID].append(itemID)
        #print(user_item)

    #extract information of each item_update
    else:
        publisherID = recBody['domainid']
        itemID = recBody['id']
        #userID = recBody['context']['simple']['57']  # might be 0 as well ;)

    if publisherID == 1677:
        print(publisherID)

    # user 0 hat nur den aktuellen artikel gelesne
    if userID != 0:
        most_similar = itemItem(user_item[publisherID], userID)
    else:
        most_similar = 0


    #counts for each publisher how often item was "touched" (in event_notification, recommendation_request or item_update)
    item_count.setdefault(publisherID, defaultdict())
    if itemID != 0:
        item_count[publisherID].setdefault(itemID, 0)
        item_count[publisherID][itemID] = item_count[publisherID][itemID]+1

    #returns most popular item (which was most often "touched")
    mostPopularItem = max(item_count[publisherID], key=item_count[publisherID].get)

    #returns sorted list of which items were most often touched
    mostPopularItems = sorted(item_count[publisherID], key=item_count[publisherID].get)

    ############################
    #building the rec-response
    ############################
    resp = {}

    if (recType=="recommendation_request"):


        #TODO erste 1000 übersprigen

        resp['recs']={}
        resp['recs']['ints']={}
        resp['recs']['ints']['3']=[]

        if publisherID == 13554:
            print(0)
        limit = recBody['limit']
        if most_similar != 0:
            for i in range(limit-1):
                try:
                    resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
                except:
                    resp['recs']['ints']['3'].append(0)
            resp['recs']['ints']['3'].append(int(most_similar))
        else:
            for i in range(limit):
                try:
                    resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
                except:
                    resp['recs']['ints']['3'].append(0)



    return app.make_response(json.dumps(resp))


if __name__ == '__main__':
    handler = RotatingFileHandler('http_flask_server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000)