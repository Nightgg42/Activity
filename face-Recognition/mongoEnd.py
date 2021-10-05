from pymongo import MongoClient, collation
import datetime
import pprint


def databaseConnection():
    client = MongoClient(
        'mongodb+srv://test123:test123@clusteractivity.oqe3k.mongodb.net/LoginDB?retryWrites=true&w=majority')
    db = client['LoginDB']
	
# input id and name into database


def inputData(ID, NAME):
    databaseConnection()
    collection = db['posts']

    post = {"id": ID,
            "name": NAME,
            "date": datetime.datetime.now()}
    log = db.Log

    if(retrieveData(ID) == True):
        post_id = posts.insert_one(post).insert_id
    else:
        print("ID already exists")

# retrieve data by ID


def retrieveData(ID):
    databaseConnection()
    collection = db['Log']
    pprint.pprint(posts.find_one({"id": ID}))

# return all documents posted in data


def retrieveAllData():
    databaseConnection()
    posts = db.posts

    for post in posts.find():
        pprint.pprint(post)


# check if an id / name exists in database
def existingData(ID):
    if(retrieveData(ID)):
        return True
    else:
        return False
