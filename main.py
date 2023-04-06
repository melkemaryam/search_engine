#!/usr/bin/env python
# coding: utf-8
import sys
sys.path.append('./models')

import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rank_bm25 import BM25Okapi
from pymongo import MongoClient
import psycopg2

from models.bm25_base import BM25_json
from models.desm import DESM_json



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



@app.get("/search")
async def search(query: str,algorithm: str):
    
    user_input = query
    

    if algorithm == 'BM25':
        out_data, raw_scores = BM25_json(user_input)
        json_data = json.dumps(out_data)

        return json_data
    
    elif algorithm == 'DESM':
        out_data, raw_scores = DESM_json(user_input)
        json_data = json.dumps(out_data)
        
        return json_data

@app.post("/feedback")
async def send_feedback(feedback):
    # Your feedback handling logic here
    print(feedback)
    return {}


