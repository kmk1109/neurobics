from flask import Flask, request, redirect, url_for, jsonify
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename

import os
import flask
import numpy as np
import json

os.makedirs(f'client/npy', exist_ok=True)
model_url = "127.0.0.1:5500"
mysql = MySQL()

app = flask.Flask(__name__)

#to display the connection status
@app.route('/', methods=['GET'])
def main():
    return "Main page Connected"
    #return render_template('main.html')

@app.route('/mpUpload', methods = ['POST'])
def mp_upload():
    if request.method == 'POST':
        data = request.json
        landmark = data['NormalizedLandmark']
        hand_info = data['LeftHand']
        exer_info = data['ExerInfo']
        hand = ""
        if hand_info == 1:
            hand = "left"
        else:
            hand = "right"        
        #landmark.save
        hand_npy = np.array(landmark)
        #np.save(os.path.join(f'client/npy', f'mp_landmark_{hand}'), hand_npy)

        #return f"hand_info"
        #print(hand)
        
        json_object={
            "LeftHand" : hand_info,
            "HandNpy" : hand_npy,
            "ExerInfo" :exer_info 
        }
        json_send = json.dumps(json_object)
        return redirect(model_url,json_send)
    else:
        return "request method is not POST"
     
#this commands the script to run in the given port
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)