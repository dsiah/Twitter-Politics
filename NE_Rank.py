import nltk
import numpy as np
import lda
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer

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

def tf_idf(tweets):
    '''
    returns a numpy matrix of tf_idf values, and a list of tweets

    parameters
    --------------------------------
    tweets : python list
        a list of tweets
    '''
    term_frequency = CountVectorizer().fit_transform(tweets)
    normalized_matrix = TfidfTransformer().fit_transform(array)
    tfidf_graph = normalized_matrix * normalized_matrix.T
    return (tfidf_graph, tweets)

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
    #unfinished
    return (model.fit_transform(X))

def text_rank(data):
    '''
    Returns a ranking of words
    
    parameters
    --------------------------
    data : tuple (numpy matrix, list)

    '''
    matrix, tweets = data[0], data[1]
    nx_graph = nx.from_scipy_sparse_matrix(matrix)
    scores = nx.pagerank(matrix)
    return sorted(((scores[i], s) for i,s in enumerate(tweets)), reverse=True)


def expand_tweet(tweet, n):
    '''
    to increase the accuracy of keywords (bc tweets are sparse)
    query search api, with tweet as search query
    take the first n search snippets

    get term-frequency matrix and get top 10 TFIDF terms

    append top 10 TFIDF terms to tweet before LDA
    '''
    pass
