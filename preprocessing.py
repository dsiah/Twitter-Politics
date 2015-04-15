import nltk
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import lda

def remove_links(source_filename, dest_filename):
    pattern = 'http://\S*|https://\S*'
    with open (source_filename, 'r+') as source, open(dest_filename, 'a') as dest:
        for line, tweet in enumerate(source, 1):
            print "Processing tweet " + str(line)
            tweet = re.sub(pattern, '', tweet)
            dest.write(tweet)

def load_tweets(source_filename):
    with open(source_filename, 'r') as source:
        tweets = [tweet.rstrip().lower() for tweet in source.readlines()]
    return tweets

def tokenize(tweet):
    tweet_tokens = nltk.word_tokenize(tweet)
    stopwords = nltk.corpus.stopwords.words('english')
    pattern = '\W*'
    for word in tweet_tokens:
        re.sub(pattern, '', word)
    tweet_tokens_processed = [word for word in tweet_tokens if word not in stopwords]
    return list(set(tweet_tokens_processed))

def count_vectorize(tweets):
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = stopwords + [ '.', ',', ':', ';', 's', '#', '@', '&', 'rt', "''", '``', 
                              '?', '!', '$', '...', "'s", "n't", "'", "--", '-', '%', '|',
                              '/', '(', ')' ]

    vectorizer = CountVectorizer(min_df=1, tokenizer=tokenize_for_vectorize, 
                                 stop_words = stopwords, ngram_range=(1,2))
    count_vector = vectorizer.fit_transform(tweets)
    print "count_vector shape: " + str(count_vector.shape)
    return (count_vector, vectorizer.get_feature_names())

def get_topics_lda(tfidf_matrix_and_vocab, tweets):
    tfidf_matrix, vocab = tfidf_matrix_and_vocab
    print "tfidf_matrix size: " + str(tfidf_matrix.shape)
    model = lda.LDA(n_topics=30, n_iter=500, random_state=1)
    model.fit(tfidf_matrix)
    topic_word = model.topic_word_
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    doc_topic = model.doc_topic_
    for i in range(30):
        print("{} (top topic: {})".format(tweets[i], doc_topic[i].argmax()))
    print doc_topic[0]
    return True


if __name__=="__main__":
    #remove_links('politician_text_test.txt', 'politician_text_processed.txt')
    tweets = load_tweets('politician_text_processed.txt')
    print tokenize_tweets_unigrams(tweets)
    #print tokenize_tweets_unigrams(tweets)
    print count_and_tf_idf(tweets)[1]
    print get_topics_lda(count_vectorize(tweets), tweets)
    #print get_topics_lda(tf_idf(count_vectorize(tweets)), tweets)

