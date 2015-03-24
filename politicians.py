import tweepy
import credentials

#Script that returns the last 500 tweets from list of politicians
if __name__ == '__main__':

    auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)
    api = tweepy.API(auth)
    #GET LIST OF POLITICIANS FROM FILE
    for tweet in tweepy.Cursor(api.user_timeline,
                                screen_name="tedcruz",
                                include_entities=False,
                                ).items(500):
            print tweet.text
