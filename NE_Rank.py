import nltk
import numpy as np
import lda
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import os
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
        contents = [x.strip('\n') for x in f.readlines()][:300]
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
    vectorizer = CountVectorizer()
    term_frequency = vectorizer.fit_transform(tweets)
    normalized_matrix = TfidfTransformer().fit_transform(term_frequency)
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
    return (model.fit_transform(X))

def text_rank(data, vocab):
    '''
    Returns a ranking of words
    
    parameters
    --------------------------------
    data : tuple (numpy matrix, list)

    '''
    matrix, tweets = data[0], data[1] # data[1] # data[1] should be vocab
    nx_graph = nx.from_scipy_sparse_matrix(matrix)
    scores = nx.pagerank(nx_graph)
    
    return sorted(((scores[i], s) for i,s in enumerate(vocab)), reverse=True)

def rank_topic(filename, rankings):
    pattern = '.txt'
    dest_filename = re.sub(pattern, '_ranking.txt', filename)
    with open('./topic_rankings/' + dest_filename, 'a+') as dest:
        for ranking in rankings:
            dest.write(ranking + '\n')
        print "Wrote to {}".format(dest_filename)

def rank_all_topics():
    for topic_file in os.listdir('./topics'):
        pass


        


if  __name__ == '__main__':

    vocab = get_vocab("politician_text_test.txt")
    tweets = load_tweets("politician_text_test.txt")
    matrix = tf_idf(vocab)

    print vocab
    print matrix[0].toarray()
    print matrix[0].shape

    rankings = text_rank(matrix, vocab)
    #rank_topic('./topics/topic0.txt', rankings)

    print rankings
