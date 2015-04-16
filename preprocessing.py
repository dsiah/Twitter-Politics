import nltk
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import lda
import collections
from pymongo import MongoClient
import matplotlib.pyplot as plt

def remove_links(source_filename, dest_filename):
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
    url_pattern = 'http://\S*|https://\S*'
    utf_pattern = '[^\x00-\x7F]+'

    count = 0
    for tweet in collection.find( {"lang":"en"} ).limit(1000000):
        count += 1
        tweet = tweet["text"]
        tweet = re.sub( url_pattern, '', tweet )
        tweet = re.sub( utf_pattern, '', tweet )
        if tweet == "":
            print "Tweet #{} is empty".format(count)
        else:
            print "Loaded tweet #{}".format(count)
            tweets.append(tweet)
    print "Loading tweets ................... Complete"
    return tweets


def tokenize(tweet):
    tweet_tokens = nltk.word_tokenize(tweet)
    stopwords = nltk.corpus.stopwords.words('english')
    pattern = '\W*'
    words = count_not_lower_than_1(tweet_tokens)
    for word in words:
        re.sub(pattern, '', word)
    tweet_tokens_processed = [word for word in words if word not in stopwords]
    return tweet_tokens_processed

def count_not_lower_than_1(tokens):
    words = []
    word_counts = collections.Counter(tokens)
    for word, count in word_counts.items():
        if count > 1 and len(word) > 2:
            words.append(word)
    return words


def count_vectorize(tweets, tokenizer_function):
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = stopwords + [ '.', ',', ':', ';', 's', '#', '@', '&', 'rt', "''", '``', 
                              '?', '!', '$', '...', "'s", "n't", "'", "--", '-', '%', '|',
                              '/', '(', ')', "amp", '[', ']', 'could', 'would', 'should',
                              'get' ]
    vectorizer = CountVectorizer(min_df=1, tokenizer=tokenizer_function, 
                                 stop_words = stopwords) #ngram_range=(1,2))
    count_vector = vectorizer.fit_transform(tweets)
    print "count_vector shape: " + str(count_vector.shape)
    return (count_vector, vectorizer.get_feature_names())

def get_topics_lda(tfidf_matrix_and_vocab, tweets):
    tfidf_matrix, vocab = tfidf_matrix_and_vocab
    print "tfidf_matrix size: " + str(tfidf_matrix.shape)
    model = lda.LDA(n_topics=45, n_iter=400, random_state=1)
    model.fit(tfidf_matrix)
    topic_word = model.topic_word_
    plt.plot(model.loglikelihoods_[5:])
    return model.doc_topic_

def write_to_topics(tweets, doc_topic):
    for i in range(len(tweets)):
        with open('./topics/topic{}.txt'.format(doc_topic[i].argmax()), 'a+') as dest:
            dest.write(tweets[i] + "\n")
            print 'writing tweet {0} to topic {1}'.format(i + 1, doc_topic[i].argmax())
    return True



if __name__=="__main__":
    #remove_links('politician_text_test.txt', 'politician_text_processed.txt')
    #tweets = load_tweets('politician_text_processed.txt')
    #print get_topics_lda(count_vectorize(tweets), tweets)
    #topics = get_topics_lda(count_vectorize(tweets), tweets)
    #write_to_topics(tweets, doc_topic)
    #print load_tweets_db('tweets3', 'apr14', 50)
    tweets = load_tweets_db('tweets3', 'apr14', 50)
    topics = get_topics_lda(count_vectorize(tweets, tokenize), tweets)
    write_to_topics(tweets, topics)

