# -*- coding: UTF-8 -*- 
from flask import Flask, request, Response
import json
import pickle
import config
import argparse
from functions import scrape_url

app = Flask(__name__)

pickle_in = open(config.WORDS_FREQUENCY_PATH, "rb")
words_frequency = pickle.load(pickle_in)

@app.route('/url_detect', methods=['POST'])
def detection():
    '''
    {
        "url" : "https://www.baidu.com"
    }
    '''

    req_body = request.json
    print(req_body)
    url = req_body["url"]
    try:
        results = scrape_url(url, words_frequency)
        if results:
            print('Predicted main category:', results[0])
            print('Predicted submain category:', results[2])
            resp = {}
            resp["category"] = results[0]
            return Response(json.dumps(resp), mimetype='application/json')
        else:
            resp = {}
            resp["category"] = "na"
            return Response(json.dumps(resp), mimetype='application/json')
    except:
            resp = {}
            resp["category"] = "na"
            return Response(json.dumps(resp), mimetype='application/json')        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
