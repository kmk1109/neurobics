from flask import Flask, request

import os
import flask
import numpy as np
import json
import requests

model_url = "http://127.0.0.1:5500"

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return "Main page Connected"

@app.route('/mpUpload', methods = ['POST'])
def mp_upload():
    if request.method == 'POST':
        data = request.json
        landmark = data['NormalizedLandmark']
        level = data['Level']
        movement = data['Movement']      

        json_redirect = [
            landmark,
            level,
            movement,
        ]
        
        res = requests.post(model_url, json=json_redirect).json()
        result = res['answer']
        
        json_return = {
            "answer" : result
        }        
        json_send_2 = json.dumps(json_return)
        return json_send_2
     
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)