import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.documents import Document
from typing import List, Dict, Any

def get_vectorstore():
    model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs=encode_kwargs
    )
    
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
    
    return vectorstore

def upsert_chunks(chunks: List[Dict[str, Any]]):
    vectorstore = get_vectorstore()
    docs = [Document(page_content=chunk["page_content"], metadata=chunk["metadata"]) for chunk in chunks]
    vectorstore.add_documents(docs)
