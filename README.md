# twitter-politico
~ *.* ~
- Note: don’t forget to install dependencies and establish app configs

##pip install list:
- tweepy
- nltk
coming soon [- pymongo]


##Obtaining a corpus of keywords
The corpus of keywords used to filter tweets from the Twitter streaming API was obtained by:
- Creating a list of the top 25 most popular American politicians on Twitter (by follower count)
- Obtaining the tweet history of each politician since the beginning of 2015 (1/01/2015)
- Extracting a list of n-grams (unigrams, bigrams, and trigrams) from the body of these tweets
- Filtering out n-grams irrelevant to politics
