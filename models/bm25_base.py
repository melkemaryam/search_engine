from rank_bm25 import BM25Okapi
from pymongo import MongoClient
import psycopg2

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

def url_documents(rel_docs):
    documents  = []
    urls = []
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
    return (documents,urls)

def BM25_json(user_query):
    out_data = {}
    rew_score_list = []
    
    rel_docs = reated_documents(user_query)
    documents , urls = url_documents(rel_docs)
    
    tokenized_corpus = [doc.split(" ") for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    
    tokenized_query = user_query.split()
    doc_scores_raw = bm25.get_scores(tokenized_query)
    doc_scores_indxed = doc_scores_raw.argsort()[::-1]
    doc_scores_indxed = doc_scores_indxed[:10]
    sorted_rawscores = doc_scores_raw[doc_scores_indxed[:10]]
    
    query = f"SELECT max(number)+1 FROM sessions;"
    cursor.execute(query)
    session_id = cursor.fetchall()[0][0]
    session_id =int(session_id)
    
    for idx,idx_score in enumerate(zip(doc_scores_indxed,sorted_rawscores),start=1):
        doc_idx, raw_score = idx_score[0], idx_score[1]
        rew_score_list.append(raw_score)
        doc_id = rel_docs[doc_idx]
        url = urls[doc_idx]
        
        text = documents[doc_idx][:600]
        out_data.update({idx:{'rank':idx,'doc_id':doc_id,'score':raw_score,'url':url,'text':text,'session_id':session_id }})  
    
    return out_data,rew_score_list