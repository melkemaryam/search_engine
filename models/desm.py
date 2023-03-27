import pickle 
import os
import scipy
import numpy as np
import json

from pymongo import MongoClient
import psycopg2
import gensim

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('gutenberg')
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from gensim.models import Word2Vec as w2v


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="SearchEngine",
    user="postgres",
    password="2580"
)

# Create a cursor object
cursor = conn.cursor()

client = MongoClient('mongodb://localhost:27017/')
# select a database
db = client['inverted_index']
mycollection = db['inverted_index']


def reated_documents(user_input):
    words = user_input.split()
    rel_docs = set()
    for word in words:
        myquery = {"word": word}
        results  = mycollection.find(myquery)
        for result in results:
            docs = result['doc_ids']
            rel_docs.update(docs)
            
    return list(rel_docs)



def get_embedding(x, out=False):
    if x in model1.wv.key_to_index:
        if out:
            return model1.syn1neg[model1.wv.key_to_index[x]]
        else:
            return model1.wv[x]
    else:
        return np.zeros(100)


model1 = gensim.models.Word2Vec.load('./models/w2v-lc.model')

def score_document(q_embeddings, doc_id,scope='in'):
    fname = f'centroid_file_{doc_id}'   
    centroid_dict = {}
    centroid_dict.update(pickle.load(open(f'./inputs/centroids/{fname}', "rb")))
    clean_centroid_dict = {k: centroid_dict[k] for k in centroid_dict if not np.isnan(centroid_dict[k][0]).any()}
    
    centroid_dict = clean_centroid_dict[fname]
    
    if scope=='in':
        centroid = centroid_dict[0]
        individual_csims = [(1 - scipy.spatial.distance.cosine(qin, centroid)) for qin in q_embeddings]
    else:
        centroid = centroid_dict[1]
        individual_csims = [(1 - scipy.spatial.distance.cosine(qin, centroid)) for qin in q_embeddings]
    return (sum(individual_csims)/len(q_embeddings))

def DESM_Scoring(user_query,scope='in'):
    query_words = user_query.split()
    rel_docs = reated_documents(user_query)
    q_embeddings = [get_embedding(x.lower()) for x in query_words]
    DESM_scores = [score_document(q_embeddings,doc,scope=scope) for doc in rel_docs]
    score_docs = list(zip(rel_docs,DESM_scores))
    score_docs = sorted(score_docs,key= lambda x:x[1],reverse=True)
    return score_docs[:10]