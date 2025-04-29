#!/usr/bin/env python

import warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import scale
from langchain_core.documents.base import Document
from langchain_openai import ChatOpenAI
from nltk.tokenize.punkt import PunktSentenceTokenizer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from glob import glob
from tqdm import tqdm
from sklearn.decomposition import PCA
# from umap import UMAP
# import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import pandas as pd
import numpy as np

import re

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

def query_db(db, query: str, k: int = 30):
    if isinstance(db, str):
        db = get_db(db)
    results = db.similarity_search_with_relevance_scores(
        query,
        k=k
    )
    df_response = pd.DataFrame([
        {
            'source': doc[0].metadata['source'],
            'sentence_idx': doc[0].metadata['sentence_idx'],
            'score': doc[1],
            'sentence': doc[0].page_content
        } for doc in results
    ])
    return df_response

def main(rootdir, k, query):
    
    BIBDIR=f'{rootdir}/bib'
    db = get_db(BIBDIR)
    SECRET=f'{rootdir}/secret.txt'
    with open(SECRET) as handle:
        secret = handle.read()
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=secret
    )
    SYSTEM=f'{rootdir}/system.txt'
    with open(SYSTEM) as handle:
        system_def = handle.read()
    
    # query = input('Query: ')
    
    df_hits = query_db(db, query, k=k)
    sources = list('[' + (df_hits.index + 1).astype(str) + '] ' + df_hits.sentence)
    context = '\n\n'.join(sources)
    
    prompt = f"""
    [QUERY]
    {query}
    
    [DOCUMENTS]
    {context}
    
    [RESPONSE]
    """
    messages = [
        (
            "system", system_def
        ),
        ("human", prompt),
    ]
    ai_msg = llm.invoke(messages).content
    
    matches = re.findall('[[][0-9]+[]]', ai_msg)
    source_indices = [
        int(match.replace('[', '').replace(']', '')) - 1
        for match in matches
    ]
    new_index_text = ['['+str(idx+1)+']' for idx in range(len(matches))]
    #for old_idx, new_idx in zip(matches, new_index_text):
    #    ai_msg = ai_msg.replace(old_idx, new_idx)
    
    l_bib = []
    
    new_ai_msg = ai_msg
    for idx, match in enumerate(matches):
        new_idx = '{'+str(idx+1)+'}'
        while new_ai_msg.find(match) != -1:
            new_ai_msg = new_ai_msg.replace(match, new_idx)
        source_bib = new_idx + f""" [{df_hits.iloc[source_indices[idx],:].source}]: {df_hits.sentence.iloc[source_indices[idx]]}"""
        l_bib.append(source_bib)
    
    output = '\n --- QUERY --- \n' + \
        query + '\n\n --- RESPONSE --- \n' + \
        new_ai_msg + '\n\n --- CITATIONS --- \n' + \
        '\n\n'.join(l_bib)
    if __name__ == '__main__':
        print(output)
    return output


from sys import argv
if __name__ == '__main__':
    rootdir, k, query = argv[1], int(argv[2]), argv[3]
    main(rootdir, k, query)
