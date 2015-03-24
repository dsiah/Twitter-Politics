import tweepy
import credentials

#Script that returns the last 500 tweets from list of politicians
if __name__ == '__main__':

    #politicians = ['barackobama', 'algore', 'senjohnmccain', 'mittromney', 'corybooker', 'gavinnewsom', 'sarahpalinusa', 'jerrybrowngov', 'reppaulryan', 'joebiden', 'govmikehuckabee', 'thehermancain', 'governorperry', 'megwhitman', 'ricksantorum', 'alfranken', 'ronpaul', 'tedcruz', 'govgaryjohnson']
    #politicians = politicians[8:]
    politicians = ['alfranken', 'ronpaul', 'tedcruz', 'govgaryjohnson']


    auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)
    api = tweepy.API(auth)
    #GET LIST OF POLITICIANS FROM FILE
    with open('politician_text.txt', 'a') as f:
       for politician in politicians:
            for tweet in tweepy.Cursor(api.user_timeline,
                                        screen_name = politician,
                                        include_entities=False,
                                        ).items(500):
                    print "currently on....... " + politician
                    tweet_encode = tweet.text.encode('ascii', 'ignore')
                    f.write(tweet_encode)
