from langchain_core.documents.base import Document
from nltk.tokenize.punkt import PunktSentenceTokenizer
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from glob import glob
from tqdm import tqdm
from sys import argv
import numpy as np
import torch

def read_sentences(mddfile: str):
    with open(mddfile) as handle:
        lines = [line for line in handle.read().split('\n') if len(line) > 0]
    sentence_tokenizer = PunktSentenceTokenizer('\n'.join(lines))
    sentences = [
        sentence.replace('\n', ' ') for sentence in
        sentence_tokenizer.sentences_from_text('\n'.join(lines))
    ]
    return  sentences

def read_docs(source):
    sentences = read_sentences(source)
    l_docs = []
    for idx, sentence in enumerate(sentences):
        doc = Document(sentence, metadata={'source': source, 'sentence_idx': idx})
        l_docs.append(doc)
    return l_docs

def chunk_iterable(iterable, max_size):
    """
    Breaks an iterable into a list of iterables with a maximum size.

    Args:
        iterable: The iterable to break into chunks.
        max_size: The maximum size of each chunk.

    Yields:
        Iterables (chunks) of the original iterable with a maximum size of max_size.
    """
    items = list(iterable)
    for i in range(0, len(items), max_size):
        yield items[i:i + max_size]

def update_db(mddpath: str, dbpath: str, model_name: str = "joe32140/ModernBERT-base-msmarco"):
    model_kwargs = {'device': 'mps' if torch.backends.mps.is_available() else 'gpu' if torch.cuda.is_available() else 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    db = Chroma(persist_directory=dbpath, embedding_function=hf)
    if model_kwargs['device'] == 'mps' or model_kwargs['device'] == 'gpu':
        if model_kwargs['device'] == 'mps':
            print('Running on Metal Performance Shaders...')
        elif model_kwargs['device'] == 'gpu':
            print('Running on GPU...')
        all_docs = []
        print('Reading in all the sentences...')
        for path in glob(f'{mddpath}/*.md'):
            all_docs += read_docs(path)
        print('Processing sentences in chunks...')
        for chunk in tqdm(list(chunk_iterable(all_docs, 1000))):
            db.add_documents(chunk)
    else:
        print('Running on CPU...')
        for path in tqdm(glob(f'{mddpath}/*.md')):
            docs = read_docs(path)
            db.add_documents(docs)
    return db

if __name__ == '__main__':
    mddpath, dbpath = argv[1], argv[2]
    update_db(mddpath, dbpath)
