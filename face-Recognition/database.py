from pymongo import MongoClient
import datetime
import pprint

client = MongoClient('mongodb+srv://test123:test123@clusteractivity.oqe3k.mongodb.net/LoginDB?retryWrites=true&w=majority')

db = client['LoginDB']
collection=db['Log']

name = input("Enter Name : ")
id = input("Enter Id : ")


post={"name":name,
	"id":id,
	"date":datetime.datetime.now()}

Log =db.Log

post_id =Log.insert_one(post).inserted_id

pprint.pprint(Log.find_one({"name":name}))