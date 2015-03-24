# Boilerplate code lifted from http://adilmoujahid.com/posts/2014/07/twitter-analytics/
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient

import json
import credentials # custom security file MUST-HAVE

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data.encode('ascii', 'ignore')) # encode to ascii to use decode json
        print tweet['text'], tweet['id']
        return True

    def on_error(self, status):
        print status

def writeToMongo (dict):
    # if type(dict) != dict: return error!
    db = client.tweets1
    collection = db.testData
    return True

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)
    stream = Stream(auth, l)
    


    stream.filter(track=['Hilary', 'Cruz', 'Politics']) 
    # TODO add more Buzzwords    
