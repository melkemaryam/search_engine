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

import sys
sys.path.append('../helpers')
from preprocessing import preprocess_text

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
    user_input = preprocess_text(user_input)
    words = user_input.split()
    rel_docs = set()
    for word in words:
        myquery = {"word": word}
        results  = mycollection.find(myquery)
        for result in results:
            docs = result['doc_ids']
            rel_docs.update(docs)
            
    return list(rel_docs)


def url_documents(rel_docs):
    documents  = []
    urls = []
    headers = []
    raw_texts = []
    for idx in rel_docs:
        query = f"SELECT * FROM sites where id = {idx};"
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            doc_id = row[0]
            url = row[1]
            urls.append(url)
            
            text = row[2]
            documents.append(text)
            
            header = row[4]
            headers.append(header)
            
            raw_text = row[5]
            raw_texts.append(raw_text)
            
    return (documents, urls, headers ,raw_texts )

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

def DESM_json(user_query,scope='in'):

    out_data = {}
    rew_score_list = []

    user_query = preprocess_text(user_query)
    query_words = user_query.split()
    
    rel_docs = reated_documents(user_query)
    documents , urls, headers , raw_texts = url_documents(rel_docs)


    q_embeddings = [get_embedding(x.lower()) for x in query_words]
    doc_scores_raw = np.array([score_document(q_embeddings,doc,scope=scope) for doc in rel_docs])

    ##normalising the scores
    doc_scores_raw = doc_scores_raw/sum(doc_scores_raw)

    doc_scores_indxed = np.array(doc_scores_raw).argsort()[::-1][:10]
    sorted_rawscores = doc_scores_raw[doc_scores_indxed]

    query = f"SELECT max(number)+1 FROM sessions;"
    cursor.execute(query)
    session_id = cursor.fetchall()[0][0]
    session_id =int(session_id)



    for idx,idx_score in enumerate(zip(doc_scores_indxed,sorted_rawscores),start=1):
        doc_idx, raw_score = idx_score[0], idx_score[1]
        rew_score_list.append(raw_score)
        doc_id = rel_docs[doc_idx]
        url = urls[doc_idx]
        
        header = headers[doc_idx]
        raw_text = raw_texts[doc_idx]
        
        out_data.update({idx:{'rank':idx,
                            'doc_id':doc_id,
                            'score':raw_score,
                            'url':url,
                            'header':header,
                            'text':raw_text,
                            'session_id':session_id 
                            }
                        })  

    # print(out_data)
    return out_data,rew_score_list