import nltk
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import lda


def remove_links(source_filename, dest_filename):
    pattern = 'http://\S*'
    with open (source_filename, 'r+') as source, open(dest_filename, 'a') as dest:
        for line, tweet in enumerate(source, 1):
            print "Processing tweet " + str(line)
            dest.write(re.sub(pattern, '', tweet))

def load_tweets(source_filename):
    with open(source_filename, 'r') as source:
        tweets = [tweet.rstrip().lower() for tweet in source.readlines()]
    return tweets

def tokenize_tweets_unigrams(tweets):
    tweet_tokens = []
    for tweet in tweets:
        tweet_tokens += nltk.word_tokenize(tweet)
    return tweet_tokens

def count_vectorize(tweets):
    vectorizer = CountVectorizer(min_df=1)
    count_vector = vectorizer.fit_transform(tweets)
    print "count_vecor shape: " + str(count_vector.shape)
    return (count_vector, vectorizer.get_feature_names())


def tf_idf(count_vector_and_vocab):
    count_vector, vocab = count_vector_and_vocab
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(count_vector)
    print "tfidf_shape : " + str(tfidf.shape)
    return (tfidf, vocab)

def count_and_tf_idf(tweets):
    vectorizer = CountVectorizer(min_df=1)
    count_vector = vectorizer.fit_transform(tweets)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(count_vector)
    print "tfidf_shape : " + str(tfidf.shape)
    return (tfidf, vectorizer.get_feature_names())

def get_topics_lda(tfidf_matrix_and_vocab, tweets):
    tfidf_matrix, vocab = tfidf_matrix_and_vocab
    print "tfidf_matrix size: " + str(tfidf_matrix.shape)
    model = lda.LDA(n_topics=30, n_iter=1500, random_state=1)
    model.fit(tfidf_matrix)
    topic_word = model.topic_word_
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    doc_topic = model.doc_topic_
    for i in range(10):
        print("{} (top topic: {})".format(tweets[i], doc_topic[i].argmax()))
    return True
'''
def get_topics_lda(count_vector_and_vocab, tweets):
    count_vector, vocab = count_vector_and_vocab
    print "count_vector: " + str(count_vector.shape)
    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(count_vector)
    topic_word = model.topic_word_
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    doc_topic = model.doc_topic_
    for i in range(10):
        print("{} (top topic: {})".format(tweets[i], doc_topic[i].argmax()))
    return True
'''



if __name__=="__main__":
    tweets = load_tweets('politician_text_preprocess.txt')
    print count_and_tf_idf(tweets)[1]
    print get_topics_lda(count_vectorize(tweets), tweets)

