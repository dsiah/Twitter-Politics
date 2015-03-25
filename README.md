# Twitter-Politico :bird:
- Note: don’t forget to install dependencies and establish app configs

##pip install list:
- tweepy
- nltk
- pymongo


##Obtaining a corpus of keywords
The corpus of keywords used to filter tweets from the Twitter streaming API was obtained by:
- Creating a list of the top 25 most popular American politicians on Twitter (by follower count)
- Obtaining the tweet history of each politician since the beginning of 2015 (1/01/2015)
- Extracting a list of n-grams (unigrams, bigrams, and trigrams) from the body of these tweets
- Filtering out n-grams irrelevant to politics

##File structure (what does what)

####credentials.py
Dependency file contains the credentials for your twitter application. You must create and register an application at Twitter (see the developers page) in order to get the 4 keys necessary to operate the tools

####db.py
Test script to start connection with local MongoDB. 

####nltk_politicians.py
A script that will grab scrape politician twitter accounts for the past week and write a list of the tweets in ...

####politician_text.txt
Text file containing the politicians tweets that were scraped in nltk_politicians

####politix.json
Junk -- streaming Twitter json objects saved in a native JSON file. Useful until mongodb database is set up and universally accessible.

####test.py
Script that opens up twitter streaming API and handles each tweet -- writes to politix.json but will be writing to local mongoDB

####tweets_to_CLI.py
Copy of test.py but does not write to DB. Instead the script prints the output to command line interface.