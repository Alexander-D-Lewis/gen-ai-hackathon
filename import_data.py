# third party
import pandas as pd
import numpy as np
from glob import iglob
from langchain.document_loaders import BSHTMLLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

if __name__ == "__main__":

    docs = []
    for file_path in iglob("downloaded_docs/*"):
        try:
            docs.extend(BSHTMLLoader(file_path=file_path).load())
            print(f"Loaded {file_path}")
        except Exception as e:
            #  print(f"Error loading {file_path}: {e}")
            pass

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, overlap=100)

    corpus_list = []

    for i, doc in enumerate(docs):
            splits = text_splitter.split_text(doc.page_content)
            corpus_list.append(splits)

    store = FAISS.from_texts(corpus_list, OpenAIEmbeddings())
    store.save_local("faiss_index")


    breakpoint()


