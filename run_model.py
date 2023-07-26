import os
import streamlit as st
import pickle
from langchain.embeddings import OpenAIEmbeddings
from langchain import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter

st.set_page_config(page_title="FCDO X LangChain: Chat with Documents", page_icon=":globe:")
st.title("FCDO Hackathon: Chat with Documents")


@st.cache_resource(ttl="1h")
def configure_qa_chain():
    query_embedding = OpenAIEmbeddings()
    db = FAISS.load_local("faiss_index_2", query_embedding)
    retriever = db.as_retriever(search_kwargs={"k": 4, "fetch_k": 8})
    #with open("faiss_store.pkl", "rb") as f:
    #    docsearch = pickle.load(f)
    #retriever=docsearch.as_retriever()
    # Create embeddings and store in vectordb
    #embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)
    # Define retriever
    #retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
    # Setup memory for contextual conversation
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # Setup LLM and QA chain
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0, streaming=True
    )
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm, retriever=retriever, memory=memory, verbose=True
    )
    return qa_chain


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container.expander("Context Retrieval")
    def on_retriever_start(self, query: str, **kwargs):
        self.container.write(f"**Question:** {query}")
    def on_retriever_end(self, documents, **kwargs):
        # self.container.write(documents)
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.container.write(f"**Document {idx} from {source}**")
            self.container.markdown(doc.page_content)
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

#uploaded_files = st.sidebar.file_uploader(
#    label="Upload PDF files", type=["pdf"], accept_multiple_files=True
#)
#if not uploaded_files:
#    st.info("Please upload PDF documents to continue.")
#    st.stop()

qa_chain = configure_qa_chain()
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
user_query = st.chat_input(placeholder="Ask me anything!")
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        cb = PrintRetrievalHandler(st.container())
        response = qa_chain.run(user_query, callbacks=[cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
print("Script finished")