from flask import Flask, render_template, request, redirect, url_for, jsonify
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

@app.route('/fileUpload', methods = ['GET','POST'])
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
    return redirect(url_for('fileUpload'))
        
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

@app.route('/upload', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file1']
        
        s_filename = secure_filename(f.filename) # 파일명 저장
        file_dir = 'uploads/' + s_filename # 파일을 저장하기 위한 경로 지정
 
        f.save('static/uploads/' + s_filename) # 파일 저장
        files = os.listdir("static/uploads")
 
        upload = {'mpdata': open('static/uploads/' + s_filename, 'rb')} # 업로드하기위한 파일
        res = requests.post('http://127.0.0.1:5000/receive', files=upload).json() # JSON 포맷, POST 형식으로 해당 URL에 파일 전송
        machineResult = res['cal_result'] # 받아온 JSON 형식의 response를 처리함
 
        # 데이터베이스 연결을 위한 connect 생성
        conn = mysql.connect()
        cursor = conn.cursor()
        # 파일명과 파일경로를 데이터베이스에 저장함
        sql = "INSERT INTO mpdata (mp_name, mp_dir) VALUES ('%s', '%s')" % (s_filename, file_dir)
        cursor.execute(sql) # sql문 입력
        data = cursor.fetchall() # 처리 결과
 
        if not data:
            conn.commit() # 수정 내용을 저장함
            return jsonify({"cal_result": machineResult}) # 결과 값 반환
 
        else:
            conn.rollback() # 수정 내용을 저장하지 않음
            return 'upload failed'
 
        # 데이터베이스와 연결 종료
        cursor.close()
        conn.close()
        
@app.route('/receive', methods=['GET', 'POST'])
def receive():
    if request.method == 'POST':
        f = request.files['mpdata'] # 보낸 파일을 받아옴
        f.save('static/images/' + secure_filename(f.filename)) # 해당 파일 저장
        files = os.listdir("static/images")
 
        # remove_background.remove('static/images/' + secure_filename(f.filename)) # 배경 제거
 
        # # 머신러닝 결과를 변수에 저장
        # predition = model.predict_food_transfer(model_transfer, test_transform, class_names, 'static/images/result.jpg')
 
        os.remove('static/images/' + secure_filename(f.filename))
 
    return jsonify({"cal_result": predition}) # 머신러닝 결과 반환


#this commands the script to run in the given port
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)