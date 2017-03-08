from flask import Flask, request

import time
import json
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict

app = Flask(__name__)
user_item = {}
item_count= {}

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

    # Interface with your recommender algorithm and build your response
    recBody = json.loads(request.form.getlist('body')[0])
    recType = request.form.getlist('type')[0]
    
    userID = recBody['context']['simple']['57']
    itemID = recBody['context']['simple']['25'] #might be 0!
    publisherID = recBody['context']['simple']['27']
    print(recType+" user:"+str(userID)+" item:"+str(itemID)+" publisher:"+str(publisherID))

    #saves for each publisher which user read what
    user_item.setdefault(publisherID, defaultdict(list))
    user_item[publisherID][userID].append(itemID)
    print(user_item)

    #counts for each publisher how often item was "touched"
    item_count.setdefault(publisherID, defaultdict())
    item_count[publisherID].setdefault(itemID,0)
    item_count[publisherID][itemID] = item_count[publisherID][itemID]+1
    mostPopularItem = max(item_count[publisherID], key=item_count[publisherID].get)
    print(item_count[publisherID])
    print(mostPopularItem)


    # predict_next_items() is a function defined somewhere in this file and contains
    # instructions to interact with your own algorithm; this is just an example!
    #algo_resp = predict_next_items(algo_handler, sessionId, prevItemId, 20)

    resp = {}
    #resp['GT'] = recRequestProperties
    #resp['rec'] = []

    # Each recommendation is a dict item of 'rec' list inside 'resp' dict and it is formed by
    # {id, rating, rank}. Response *must* follow this structure to be readable by the evaluator
    #for i in range(len(algo_resp)):
    #    resp['rec'].append({"id": int(algo_resp[i][0]), "rating": float(algo_resp[i][1]), "rank": i+1})

    return app.make_response(json.dumps(resp))

if __name__ == '__main__':
    handler = RotatingFileHandler('http_flask_server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000)
