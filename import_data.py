# std
import os

# third party
import pandas as pd
import numpy as np
from glob import iglob
from langchain.document_loaders import UnstructuredODTLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from tqdm import tqdm
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")



def fix_for_nltk_error():
    import nltk
    import ssl

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # you'll want to download punkt and perceptron_tagger
    nltk.download()



def load_docs():
    docs = []
    
    for file_path in tqdm(iglob("downloaded_docs/downloaded_docs/*.odt")):
        try:
            docs.extend(UnstructuredODTLoader(file_path=file_path).load())

        except Exception as e:
            print(f"Failed to load {file_path}: {e}")

    return docs


def split_docs(docs):
    text_splitter = CharacterTextSplitter()

    corpus_list = []

    for doc in tqdm(docs):
            splits = text_splitter.split_text(doc.page_content)
            corpus_list.append(splits)
    return corpus_list



if __name__ == "__main__":
    docs = load_docs()
    corpus_list = split_docs(docs)
    
    store = FAISS.from_texts(corpus_list, OpenAIEmbeddings(openai_organization="DS Hack n",
                                                           openai_api_key=openai_api_key))
    store.save_local("faiss_index")


    breakpoint()


