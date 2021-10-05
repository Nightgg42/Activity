# main working face detector uses MONGO
import cv2
import numpy as np
import os
from pymongo import MongoClient
from datetime import datetime
import pprint
import requests, urllib.parse
import pandas as pd

client = MongoClient(
        'mongodb+srv://test123:test123@clusteractivity.oqe3k.mongodb.net/LoginDB?retryWrites=true&w=majority')
db = client['LoginDB']

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingData.xml")
#font = cv2.InitFont(cv2.CV_FONT_HERSHEY_COMPLEX_SMALL,5,1,0,4)
fontface = cv2.FONT_HERSHEY_PLAIN
fontscale = 1
fontcolor = (0, 0, 0)
progress = 0
state = 0
id = 0
key = 0
time = datetime.now().timestamp()

token = "8BVVzQVt0b9e3j1iTSiSd9LKgaB7RuWK1unT8nWx54J"
url = 'https://notify-api.line.me/api/notify'
HEADERS = {'Authorization': 'Bearer ' + token}

def getActivity():
    data = db["data"]
    for x in data.find():
        if (datetime.strptime(x['endTime'], '%Y-%m-%dT%H:%M').microsecond - datetime.strptime(x['startTime'], '%Y-%m-%dT%H:%M').microsecond < 0): return x
    return {'count': 0}

def getProfile(id):
    posts = db["posts"]

    #print(posts.find_one({'id': id}))

    return posts.find_one({'id': id})

def send(id):
    Log = db["Log"]
    data = db["data"]
    name = getProfile(id)["name"]
    activity = getActivity()
    date = datetime.now()

    post = {"name": name, "id": id, "date": date}

    msg = "{}-{}-{}".format(id, name, date)
    Log.insert_one(post).inserted_id
    data.update_one(activity, {'$set': {'count': activity['count']+1}})
    requests.post(url, headers=HEADERS, params={"message": msg})

    print('success')

def inTime():
    date = datetime.now()
    if (date.hour == 16): return True
    else: return False

def confirm(id):
    cv2.rectangle(img, (50, 50), (280, 100), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (50, 50), (280, 100), (0, 0, 0), 2)
    cv2.putText(img, "Your ID is {}".format(id), (80, 80) , fontface, fontscale, (0, 0, 0))
    send(id)

while True:
    key = cv2.waitKey(1)
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    name = ""
    if (True and state == 0):
        for(x, y, w, h) in faces:
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            # id=getNm(id)
            if(conf >= 4 and conf <= 100): # Matched
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                if (len(faces) == 1): progress += 1
                cv2.putText(img, str(id), (x, y+h+30),
                    fontface, fontscale, (0, 255, 0))
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "unknown", (x, y+h+50), fontface,
                    fontscale, (0, 0, 255))
    if (len(faces) == 0): progress = 0
    if (state == 0 and progress == 25): 
        state = 1
    if (state == 1): 
        confirm(str(id))
        state = 2
        time = datetime.now().timestamp()
    if (state == 2):
        cv2.rectangle(img, (50, 50), (280, 100), (255, 255, 255), cv2.FILLED)
        cv2.rectangle(img, (50, 50), (280, 100), (0, 0, 0), 2)
        cv2.putText(img, "Your ID is {}".format(id), (80, 80) , fontface, fontscale, (0, 0, 0))
    if (state == 2 and len(faces) == 0 and datetime.now().timestamp() - time > 2): 
        state = 0
    print(datetime.now().timestamp() - time)
		
    cv2.imshow("Face", img)
    if(key == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()
