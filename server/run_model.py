from flask import Flask, request, redirect, url_for, jsonify
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
#from restruct_npy import restruct_npy

import flask
import numpy as np
import json

from tensorflow.keras.models import load_model

model_exer1 = load_model(f'../models/exer1/classifier_acc_raw.h5')
model_exer2 = load_model(f'../models/exer2/classifier_acc_raw.h5')
model_exer3 = load_model(f'../models/exer3/classifier_acc_raw.h5')

def restruct_npy(_joint):
    joint = _joint
    data = []
    
    # Compute angles between joints
    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
    v = v2 - v1 #[20,3]
    # Normalize v
    v = v / np.linalg.norm(v, axis=1)[:,np.newaxis]

    # Get angle using arcos of dot product
    angle = np.arccos(np.einsum('nt,nt->n',
        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

    angle = np.degrees(angle) # Convert radian to degree

    angle_reshape = np.array([angle], dtype=np.float32)

    d = np.concatenate([joint.flatten(), angle_reshape.flatten()])

    data.append(d)
    data = np.array(data)
    input_data = np.expand_dims(np.array(data[0], dtype=np.float32), axis=0)
    return input_data

model_app = flask.Flask(__name__)

@model_app.route("/", methods = ['POST'])
def exer_select_and_play():
    if request.method == 'POST':
        data = request.json
        hand_npy = data[0]
        level = data[1]
        movement = data[2]
   
        hand_npy = np.array(hand_npy)
        hand_npy = restruct_npy(hand_npy)

        if level == 1:
            actions = [1,2] # ['thumb','little']
            y_pred = model_exer1.predict(hand_npy).squeeze()
            i_pred = int(np.argmax(y_pred))
            action = actions[i_pred]
            if action == movement:
                data = {'answer' : 1}
                return jsonify(data)
            else:
                data = {'answer' : -1}
                return jsonify(data)  
                
        elif level == 2:
            actions = [1,2] #['thumb','paper']
            y_pred = model_exer2.predict(hand_npy).squeeze()
            i_pred = int(np.argmax(y_pred))
            action = actions[i_pred]            
            if action == movement:
                data = {'answer' : 1}
                return jsonify(data)
            else:
                data = {'answer' : -1}
                return jsonify(data)      
        else :
            actions = [1,2,3,4,5,6]#['five','four','three','two','one', 'zero']
            y_pred = model_exer3.predict(hand_npy).squeeze()
            i_pred = int(np.argmax(y_pred))
            action = actions[i_pred]            
            if action == movement:
                data = {'answer' : 1}
                return jsonify(data)
            else:
                data = {'answer' : -1}
                return jsonify(data)         
            
if __name__ == '__main__':
    model_app.run(host="127.0.0.1", port=5500, debug=True)