from flask import Flask, request

import time
import json
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict
import numpy as np

app = Flask(__name__)
user_item = {}
item_count= {}
allItems={}

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

def user_user_collaborative(user_item_publisher, allItems):
    #print(np.shape(user_item_publisher[0])) 
    #print(np.shape(allItems[1]))
    #print (allItems)
    print(np.shape(user_item_publisher[0])[0])
    print(np.shape(allItems[1])[0])
    similarity=np.zeros((np.shape(user_item_publisher[0])[0],np.shape(allItems[1])[0]))
    for i in range (np.shape(user_item_publisher[0])[0]):
        for j in range (len(allItems)):
            if allItems[j] in user_item_publisher[i]:
                similarity[i][j]=1
    print (similarity)
                
                
    
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
        user_item[publisherID][userID].append(itemID)
        #print(user_item)
        
        allItems.setdefault(publisherID, defaultdict(list))
        allItems[publisherID][1].append(itemID)
        #print(allItems)
        
        user_user_collaborative(user_item[publisherID], allItems[publisherID]);


    #extract information of each item_update
    else:
        publisherID = recBody['domainid']
        itemID = recBody['id']


    #counts for each publisher how often item was "touched" (in event_notification, recommendation_request or item_update)
    item_count.setdefault(publisherID, defaultdict())
    item_count[publisherID].setdefault(itemID,0)
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
        resp['recs']={}
        resp['recs']['ints']={}
        resp['recs']['ints']['3']=[]

        limit = recBody['limit']
        print ("limit"+str(limit))
        for i in range(limit):
            try:
                resp['recs']['ints']['3'].append(int(mostPopularItems[i]))
            except:
                resp['recs']['ints']['3'].append(0)

        print(resp)

    return app.make_response(json.dumps(resp))

if __name__ == '__main__':
    handler = RotatingFileHandler('http_flask_server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000)