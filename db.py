from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# test db is tweets1, collection is testData
db = client.tweets1
collection = db.testData