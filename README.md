# search_engine
Design and implementation of a search engine using specific information retrieval methods

![Picture1](https://github.com/melkemaryam/search_engine/assets/32023419/d83cdeb1-3ae9-4337-b5cf-82b4450dfc51?raw=true)


# News Article Information Retrieval System

## Introduction
This project focuses on designing an Information Retrieval (IR) system tailored for news articles. By leveraging advanced IR techniques and models, our goal is to provide a robust and efficient system for retrieving news articles with high relevance and accuracy. Our system is designed to improve the quality of search results, ensuring timely and reliable information dissemination.

## System Design
We target two levels of complexity in search results:
1. **General News**: The query will be applied across all available articles.
2. **Sports News**: Concentrating on a telescoped dataset, focusing on sports-related articles.

## Dataset
- **Source**: BBC News articles scraped using Python, categorized under “/news” and “/sports”.
- **Period**: Articles are scraped over a 10-day window to ensure a diverse range of queries and relevancy.
- **Challenges**: Overcoming the lack of queries and relevancies through self-labelling and other methods.

## Architecture
Our architecture comprises three main components:
1. **Document Handler**: Processes and indexes documents.
2. **Query Handler**: Manages query preprocessing.
3. **Retrieval Handler**: Executes document retrieval based on query-document relevance.

![Search Engine Framework](<link-to-figure-B-image>)

## Software and Tools
- **Front-End**: FastAPI for capturing and responding to user queries.
- **Back-End**: Python, PostgreSQL, MongoDB, and several libraries like Spacy, Beautiful Soup, psycopg2, pymongo, and rank_bm25.

![Tech Stack](https://github.com/melkemaryam/search_engine/assets/32023419/d83cdeb1-3ae9-4337-b5cf-82b4450dfc51?raw=true)

## Investigation
Focusing on BM25 and DESM models, including a mixture model, to evaluate performance on broad and telescoped datasets.

## References
- Saracevic, T. (2010). [Relevance in IR](<link-to-paper>).
- Nalisnick, E. et al. (2016). [Improving document ranking with dual word embeddings](<link-to-paper>).
- Järvelin, K. and Kekäläinen, J. (
