#!/usr/bin/env python

from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import Chroma
from langchain_chroma import Chroma
from sys import argv
import pandas as pd

def get_db(dbpath: str, model_name: str = "joe32140/ModernBERT-base-msmarco"):
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    db = Chroma(persist_directory=dbpath, embedding_function=hf)
    return db

def query_db(dbpath: str, csvpath: str, query: str, k: int = 50):
    db = get_db(dbpath)
    results = db.similarity_search_with_relevance_scores(query, k=k)
    df_response = pd.DataFrame([
        {
            'source': doc[0].metadata['source'],
            'sentence_idx': doc[0].metadata['sentence_idx'],
            'score': doc[1],
            'sentence': doc[0].page_content
        } for doc in results
    ])
    df_response.to_csv(csvpath)

if __name__ == '__main__':
    dbpath, csvpath, query, k = argv[1], argv[2], argv[3], int(argv[4])
    query_db(dbpath, csvpath, query, k)
