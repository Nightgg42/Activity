"""
	code creates a dataset of images to be trained by opening camera and capturing
	20 images of a detected face 
	also takes input of user id and name of persons face and inserts into a database
"""
import cv2
import numpy as np
import os
from pymongo import MongoClient
import datetime
import pprint


def inputData(ID,NAME):
	client = MongoClient('mongodb+srv://test123:test123@clusteractivity.oqe3k.mongodb.net/LoginDB?retryWrites=true&w=majority')
	db=client['LoginDB']
	collection=db['Log']

	post={"id":ID,
	 "name":NAME,
	 "date":datetime.datetime.now()}
	Log=db.Log
	posts=db.posts

	post_id=posts.insert_one(post)

def retrieveData(ID):
	client = MongoClient('mongodb+srv://test123:test123@clusteractivity.oqe3k.mongodb.net/LoginDB?retryWrites=true&w=majority')
	db=client['LoginDB']
	collection=db['Log']
	posts=db.posts

	pprint.pprint(posts.find_one({"id":ID}))

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)

id=input('Please Enter Student ID:')
name=input('Please Enter your name and lastname:')

inputData(id,name)
retrieveData(id)

sampleNum=0

while True:
	ret,img=cam.read()
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces=faceDetect.detectMultiScale(gray,1.3,5)
	for(x,y,w,h) in faces:
		sampleNum+=1
		cv2.imwrite("dataset/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
		cv2.waitKey(100)
	cv2.imshow("Face",img)
	cv2.waitKey(1)
	if(sampleNum>20):
		break

cam.release()
cv2.destroyAllWindows()
