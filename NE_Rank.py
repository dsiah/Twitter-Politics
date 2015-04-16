import nltk
import numpy as np
import lda
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import os
import re
from preprocessing import tokenize, count_vectorize

def load_tweets(source_file):
    '''
    returns a list of strings stripped of newlines

    parameters
    -------------------------
    source_file
        file containing strings(tweets) separated by newlines
    '''
    with open(source_file, 'r+') as f:
        contents = [x.strip('\n') for x in f.readlines()]
    return contents

def get_vocab(source_file):
    '''
    returns a list of tokens from the source file

    parameters
    -----------------------
    source_file
        file containing strings separated by newlines
    '''
    contents = load_tweets(source_file)
    contents = ' '.join(contents)
    return nltk.word_tokenize(contents)

def tf_idf(data_and_vocab):
    '''
    returns a numpy matrix of tf_idf values, and a list of tweets

    parameters
    --------------------------------
    tweets : python list
        a list of tweets
    '''
    term_frequency, vocab = data_and_vocab
    normalized_matrix = TfidfTransformer().fit_transform(term_frequency)
    tfidf_graph = normalized_matrix.T * normalized_matrix
    return (tfidf_graph, vocab)

def get_topics_lda(X, n_topics, n_iter=500, random_state=1):
    '''
    Documentation can b found at https://aridell.org/lda.html

    Latent Dirichlet allocation using collapsed Gibbs sampling

    Returns an adjacency list of words
    - Each array represents a list of words from a single topic
    - Each subarray is a list of words corresponding to a topic

    Parameters:
    __________________________________

    X : numpy array
        A document-term matrix : Sparse matrices are accepted

    n_iter : int, default 2000
        Number of sampling iterations

    alpha: float, default 0.1
        Dirichlet parameter for distibution over topics

    '''
    model = lda.LDA(n_topics, n_iter)
    return (model.fit_transform(X))

def text_rank(data_and_vocab):
    '''
    Returns a ranking of words
    
    parameters
    --------------------------------
    data : tuple (numpy matrix, list)

    '''
    data, vocab = data_and_vocab
    nx_graph = nx.from_scipy_sparse_matrix(data)
    scores = nx.pagerank(nx_graph)
    return sorted(((scores[i], s) for i,s in enumerate(vocab)), reverse=True)

def rank_topic(filename, rankings):
    pattern = '.txt'
    dest_filename = re.sub(pattern, '_ranking.txt', filename)
    
    with open(dest_filename, 'a+') as dest:
        
        for ranking in rankings:
            dest.write(str(ranking[0]))
            dest.write(' , ')
            dest.write(ranking[1])
            dest.write('\n')
            
        print "Completed write to {}".format(dest_filename)

def rank_all_topics():
    topic_files = [topicfile for topicfile in os.listdir('./topics') if topicfile[-4:] == '.txt']
    for topic_file in topic_files:
        topic_file = './topics/' + topic_file
        tweets = load_tweets(topic_file)
        data_and_vocab = count_vectorize(tweets, tokenize)
        tfidf_and_vocab = tf_idf(data_and_vocab)
        rankings = text_rank(tfidf_and_vocab)
        rank_topic(topic_file, rankings)




if  __name__ == '__main__':
    """
    tweets = load_tweets("./topics/topic0.txt")
    data_and_vocab = count_vectorize(tweets, tokenize)
    matrix_and_vocab = tf_idf(data_and_vocab)
    print matrix_and_vocab[0].toarray()
    print matrix_and_vocab[0].shape
    rankings = text_rank(matrix_and_vocab)
    rank_topic('./topics/topic0.txt', rankings)
    """
    rank_all_topics()
