#!/usr/bin/env python
# coding: utf-8


import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]



app = FastAPI()

# Add the following lines to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient('mongodb://localhost:27017/')
db = client['inverted_index']
mycollection = db['inverted_index']



@app.get("/search")
async def search(query: str,algorithm: str):
    # Your search logic here
    user_input = query
    # print(algorithm)

    if algorithm == 'BM25':
        words = user_input.split()
        rel_docs = set()
        for word in words:
            myquery = {"word": word}
            results  = mycollection.find(myquery)
        for result in results:
            docs = result['doc_ids']
            print(word,docs)
            rel_docs.update(docs)

        rel_docs = list(rel_docs)
        documents  = []
        urls = []
        print(rel_docs)
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

        tokenized_corpus = [doc.split(" ") for doc in documents]

        bm25 = BM25Okapi(tokenized_corpus)

        tokenized_query = words
        doc_scores_raw = bm25.get_scores(tokenized_query)
        doc_scores = doc_scores_raw.argsort()[::-1]
        doc_scores = doc_scores[:10]
        out_data = []
        
        for idx,score_id in enumerate(doc_scores,start=1):
            doc_id = rel_docs[score_id]
            url = urls[score_id]
            text = documents[score_id][:600]
            out_data.append({'rank':idx,'doc_id':doc_id,'url':url,'text':text })

        json_data = json.dumps(out_data)

        # Example: Use the query to search your data and return the relevant results as a JSON object
        search_results = json_data

        return search_results
    
    # elif algorithm == 'DESM':
        
    

@app.post("/feedback")
async def send_feedback(feedback):
    # Your feedback handling logic here
    print(feedback)
    return {}


