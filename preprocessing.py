import nltk
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import lda
from pymongo import MongoClient
import codecs

def remove_links(source_filename, dest_filename):
    pattern = 'http://\S*|https://\S*'
    with open (source_filename, 'r+') as source, open(dest_filename, 'a') as dest:
        for line, tweet in enumerate(source, 1):
            print "Processing tweet " + str(line)
            tweet = re.sub(pattern, '', tweet)
            dest.write(tweet)

def preprocess(tweet):
    pass

def load_tweets(source_filename):
    with open(source_filename, 'r') as source:
        tweets = [tweet.rstrip().lower() for tweet in source.readlines()]
    return tweets

def load_tweets_db(db_name, table_name, num):
    client = MongoClient()
    db = client[db_name]
    collection = db[table_name]
    tweets = []
    url_pattern = "http://\S*|https://\S*"
    utf_pattern = "[^\x00-\x7F]+"
    
    for tweet in collection.find().limit(100000):
        tweet = re.sub(utf_pattern, '', tweet)
        tweet = re.sub(url_pattern, '', tweet)
        tweets.append(tweet["text"])
    return tweets


def tokenize(tweet):
    tweet_tokens = nltk.word_tokenize(tweet)
    stopwords = nltk.corpus.stopwords.words('english')
    pattern = '\W*'
    for word in tweet_tokens:
        re.sub(pattern, '', word)
    tweet_tokens_processed = [word for word in tweet_tokens if word not in stopwords]
    return list(set(tweet_tokens_processed))

def count_vectorize(tweets, tokenizer_function):
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = stopwords + [ '.', ',', ':', ';', 's', '#', '@', '&', 'rt', "''", '``', 
                              '?', '!', '$', '...', "'s", "n't", "'", "--", '-', '%', '|',
                              '/', '(', ')' ]
    vectorizer = CountVectorizer(min_df=1, tokenizer=tokenizer_function, 
                                 stop_words = stopwords) #ngram_range=(1,2))
    count_vector = vectorizer.fit_transform(tweets)
    print "count_vector shape: " + str(count_vector.shape)
    return (count_vector, vectorizer.get_feature_names())

def get_topics_lda(tfidf_matrix_and_vocab, tweets):
    tfidf_matrix, vocab = tfidf_matrix_and_vocab
    print "tfidf_matrix size: " + str(tfidf_matrix.shape)
    model = lda.LDA(n_topics=30, n_iter=500, random_state=1)
    model.fit(tfidf_matrix)
    topic_word = model.topic_word_
    return model.doc_topic_

def write_to_topics(tweets, doc_topic):
    for i in range(len(tweets)):
        with open('./topics/topic{}.txt'.format(doc_topic[i].argmax()), 'a+') as dest:            
            dest.write(tweets[i])
            dest.write('\n')
            print 'writing tweet {0} to topic {1}'.format(i + 1, doc_topic[i].argmax())
    return True



if __name__=="__main__":

    tweets = load_tweets_db('tweets3', 'apr14', 50)
    topics = get_topics_lda(count_vectorize(tweets, tokenize), tweets)
    write_to_topics(tweets, topics)
