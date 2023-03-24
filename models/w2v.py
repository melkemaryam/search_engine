import pickle 
import os
import scipy
import numpy as np
import json


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

def get_embedding(x, out=False):
    if x in model1.wv.key_to_index:
        if out:
            return model1.syn1neg[model1.wv.key_to_index[x]]
        else:
            return model1.wv[x]
    else:
        return np.zeros(100)



# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="SearchEngine",
    user="postgres",
    password="2580"
)
cursor = conn.cursor()

query = f"SELECT content FROM sites;"
cursor.execute(query)
results = cursor.fetchall()

sw = stopwords.words('English') # this is a list of stopwords
# Function to remove stopwords per line if they are present in the line
def rem_stops_line(line, words):
    if len(line) >1:
        return [w for w in line if w not in words]
    else:
        return line

# Remove stop words for an entire text. Separate functions make it easier to parallelize if required.
def remove_stops(text, words = sw):
    return [rem_stops_line(line, words) for line in text]

lines = [line[0].rstrip('\n').lower() for line in results]
lines = [line.translate(str.maketrans('', '', string.punctuation)) for line in lines]
lines = [word_tokenize(line) for line in lines]
filtered_lines = remove_stops(text = lines, words = sw)

model1 = w2v(
    filtered_lines,
    min_count=3,
    sg = 1,       # 1 for skip-gram, 0 for cbow
    window=7   # sliding window size
)

model1.save('./models//w2v-lc.model')
model1.wv.save_word2vec_format('./models/w2v-lc.model.bin', binary=True)

vocab =  model1.wv.key_to_index

with open('./models/w2v-lc-vocab.json', 'w') as f:
    f.write(json.dumps(vocab))


#creating doc vector
query = f"SELECT id,content FROM sites;"
cursor.execute(query)
results = cursor.fetchall()

for document in results:
    line = document[1]
    id_ = document[0]
    fname = f'centroid_file_{id_}'
    
    centroid_in = (np.mean(np.array([get_embedding(x) for x in nltk.word_tokenize(line.lower())]), axis=0))
    centroid_out = (np.mean(np.array([get_embedding(x, out=True) for x in nltk.word_tokenize(line.lower())]), axis=0))
    
    out_dict = { fname : (centroid_in, centroid_out) }
    pickle_file = './inputs/centroids/' + os.path.basename(fname).replace('.txt', '.p')
    pickle.dump(out_dict, open(pickle_file, "wb"))