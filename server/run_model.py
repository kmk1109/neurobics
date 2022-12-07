from flask import Flask, request, redirect, url_for, jsonify
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
from restruct_npy import restruct_npy

import flask
import numpy as np
import json

from tensorflow.keras.models import load_model

model_exer1 = load_model(f'models/exer1/classifier_acc_raw.h5')
model_exer2 = load_model(f'models/exer2/classifier_acc_raw.h5')
model_exer3 = load_model(f'models/exer3/classifier_acc_raw.h5')


model_app = flask.Flask(__name__)

@model_app.route("/", methods = ['POST'])
def exer_select_and_play():
    if request.method == 'POST':
        data = request.json
        hand_npy = data['HandNpy']
        hand_info = data['LeftHand']
        exer_info = data['ExerInfo']
        answer = data['Answer']
        
        hand_npy = restruct_npy(hand_npy)
        
        iscorrect = 0
        
        if exer_info == 1:
            actions = ['thumb','little']
            y_pred = model_exer1.predict(hand_npy).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]
            action = actions[i_pred]
            if action == answer:
                iscorrect = 1
                return iscorrect
        elif exer_info == 2:
            actions = ['five','four','three','two','one']
            y_pred = model_exer2.predict(hand_npy).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]
            action = actions[i_pred]
            if action == answer:
                iscorrect = 1
                return iscorrect            
        else :
            actions = ['thumb','paper']
            y_pred = model_exer3.predict(hand_npy).squeeze()
            i_pred = int(np.argmax(y_pred))
            conf = y_pred[i_pred]
            action = actions[i_pred]
            if action == answer:
                iscorrect = 1
                return iscorrect            
        
        # json_object={
        #     "LeftHand" : hand_info,
        #     "HandNpy" : hand_npy,
        #     "ExerInfo" :exer_info 
        # }        
        
        # json_send = json.dump(json_object)
        # if exer_info == 1:
        #     return redirect(url_for("127.0.0.1:5501", isLeft = hand_info, npy = hand_npy))
        # elif exer_info == 2:
        #     return redirect("127.0.0.1:5502", json_send)
        # elif exer_info == 3:
        #     return redirect("127.0.0.1:5503", json_send)

if __name__ == '__main__':
    model_app.run(host="127.0.0.1", port=5500, debug=True)