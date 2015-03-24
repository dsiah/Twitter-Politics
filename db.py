from pymongo import MongoClient

# change localhost to the IP of the machine
client = MongoClient('localhost', 27017)

# test db is tweets1, collection is testData
db = client.tweets1
collection = db.testData

#more comments
listo = collection.find()

for i in listo:
	print i, "\n"