from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename

import os
import flask
import requests

mysql = MySQL()

app = flask.Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_MP'] = 'mpdata'
app.config['MYSQL_DATABASE_ANSWER'] = 'answer'
app.config['MYSQL_DATABASE_RESULT'] = 'result' #only show correct/wrong, result is detiermied by result of mpdata and answer
app.secret_key = "NEUROBICS"
mysql.init_app(app)

#to display the connection status
@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')
def handle_call():
    return "Successfully Connected"

#the get method. when we call this, it just return the text "Hey!! I'm the fact you got!!!"
@app.route('/getfact', methods=['GET'])
def get_fact():
    return "Hey!! I'm the fact you got!!!"

#the post method. when we call this with a string containing a name, it will return the name with the text "I got your name"
@app.route('/getname/<name>', methods=['POST'])
def extract_name(name):
    return "I got your name "+name;

@app.route('/upload/', methods = ['GET','POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save('static/uploads/'+secure_filename(f.filename))
        files = os.listdir("static/uploads")
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "INSERT INTO mpdata (mp_name, mp_dir) VALUE('%s', '%s')" % (secure_filename(f.filename), 'uploads/'+secure_filename(f.filename))
        cursor.execute(sql)
        data = cursor.fetchall()
        
        if not data:
            conn.commit()
            return redirect(url_for("main"))
        
        else:
            conn.rollback()
            return 'upload failed'
        
        cursor.close()
        conn.close()
        
@app.route('/view', methods = ['GET', 'POST'])
def view():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT mp_name, mp_dir FROM mpdata"
    cursor.execute(sql)
    data = cursor.fetchall()
    
    data_list = []
    
    for obj in data:
        data_dic = {
            'name':obj[0],
            'dir':obj[1]
        }        
        data_list.append(data_dic)
        
    cursor.close()
    conn.close()
    
    return redirect(url_for("main"))

#this commands the script to run in the given port
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)