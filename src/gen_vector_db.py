from langchain_core.documents.base import Document
from nltk.tokenize.punkt import PunktSentenceTokenizer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from glob import glob
from tqdm import tqdm
from sys import argv
import numpy as np

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

def update_db(mddpath: str, dbpath: str, model_name: str = "joe32140/ModernBERT-base-msmarco"):
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    db = Chroma(persist_directory=dbpath, embedding_function=hf)
    for path in tqdm(glob(f'{mddpath}/*.md')):
        docs = read_docs(path)
        db.add_documents(docs)
    return db

if __name__ == '__main__':
    mddpath, dbpath = argv[1], argv[2]
    update_db(mddpath, dbpath)