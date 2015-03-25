from pymongo import MongoClient

# change localhost to the IP of the machine
client = MongoClient('153.104.156.100', 27017)

# test db is tweets1, collection is testData
db = client.tweets1
collection = db.testData

#more comments
listo = collection.find()

class PoliticsDB:

	def __init__(self, ipaddress):
		self.ipaddress = ipaddress

pdb = PoliticsDB(129391923)
