import sqlite3
import json
import random
import time
from datetime import datetime
import time
import pyrebase
import sys
from flask import Flask,request, jsonify,Response,render_template

config={
    "apiKey": "AIzaSyAHUhDRcIwuZGvTPEhvG1zUpLet__98joI",
    "authDomain": "ahmsbashe.firebaseapp.com",
    "databaseURL": "https://ahmsbashe.firebaseio.com",
    "projectId": "ahmsbashe",
    "storageBucket": "ahmsbashe.appspot.com",
    "messagingSenderId": "476523736767",
    "appId": "1:476523736767:web:3b5ca6351dc19ac387e00a"

}
firebase = pyrebase.initialize_app(config)
def Hrt():
    cone=sqlite3.connect('/home/pi/Desktop/Bingo/AHMS.db')
    cure=cone.cursor()
    cure.execute("SELECT bpm FROM Heart_Rate ORDER BY rDatetime DESC LIMIT 1")
    BP = cure.fetchall()
    hear, = BP[0]
    return hear


def tmp():
    cone=sqlite3.connect('/home/pi/Desktop/Bingo/AHMS.db')
    cure=cone.cursor()
    cure.execute("SELECT temp FROM Rectal_Temp ORDER BY rDatetime DESC LIMIT 1")
    Tp = cure.fetchall()
    tpr, = Tp[0]
    return tpr


db = firebase.database()
app = Flask(__name__)
random.seed() 

@app.route("/temp")
def get_temp():
    data = request.args['data']
    conn=sqlite3.connect('/home/pi/Desktop/Bingo/AHMS.db')
    curs=conn.cursor()
    curs.execute("""INSERT INTO Rectal_Temp values(datetime('now','localtime'),(?))""",(data,))
    conn.commit()
    curs.execute("SELECT bpm FROM Heart_Rate ORDER BY rDatetime DESC LIMIT 1")
    BPM = curs.fetchall()
    heart, = BPM[0]
    db.child('data').push({"a":float(data),"b":heart,"time":int(time.time()*1000)});
    conn.close()
    return jsonify(data)

@app.route("/bpm")
def get_bpm():
    data = request.args['data']
    conn=sqlite3.connect('/home/pi/Desktop/Bingo/AHMS.db')
    curs=conn.cursor()
    curs.execute("""INSERT INTO Heart_Rate values(datetime('now','localtime'),(?))""",(data,))
    conn.commit()
    curs.execute("SELECT temp FROM Rectal_Temp ORDER BY rDatetime DESC LIMIT 1")
    TEMP = curs.fetchall()
    rectal, = TEMP[0]
    db.child('data').push({"a":rectal,"b":int(data),"time":int(time.time()*1000)});
    conn.close()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chart-data")
def chart_data():
    def generate_random_data():
        while True:
            con = sqlite3.connect('/home/pi/Desktop/Bingo/AHMS.db')
            curs=con.cursor()
            con.commit()
            curs.execute("SELECT bpm FROM Heart_Rate ORDER BY rDatetime DESC LIMIT 1")
            BPM = curs.fetchall()
            heart, = BPM[0] 
            curs.execute("SELECT temp FROM Rectal_Temp ORDER BY rDatetime DESC LIMIT 1")
            TEMP = curs.fetchall()
            rectal, = TEMP[0]
            con.close()
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value':float(tmp()), 'value1': int(Hrt())})
            yield f"data:{json_data}\n\n"
            time.sleep(10)

    return Response(generate_random_data(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug = True,threaded = True)
