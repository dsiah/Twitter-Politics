from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser(description='Set the IP address')
parser.add_argument('ip_address', help='Mandatory: IP Address of mongodb server', 
                        action='store')



# change localhost to the IP of the machine
class PoliticsDB:

    def __init__ (self, ipaddress):
        self.ipaddress = ipaddress
        self.client = MongoClient(ipaddress, 27017)
        self.db = self.client.tweets1
        self.collection = self.db.testData

    def getInfo (self):
        print self.db
        print self.collection
        print self.ipaddress


    if __name__ == '__main__':
        args = parser.parse_args()	
        #print args.ip_address
        pdb = PoliticsDB(args.ip_address)
