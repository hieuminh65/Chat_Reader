import streamlit as st
from dotenv import load_dotenv 
from PyPDF2 import PdfReader
import docx2txt
from langchain.agents import create_csv_agent
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from html_css import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = ""
    for pdf_doc in pdf_docs:
        pdf_reader = PdfReader(pdf_doc)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_docx_text(docx_docs):
    text = docx2txt.process(docx_docs)
    return text

def get_txt_text(txt_docs):
    text = txt_docs.read().decode("utf-8")
    return text

def get_csv_answer(csv_docs, question):
    agent = create_csv_agent(OpenAI(temperature=0.3), csv_docs, verbose=True)
    answer = agent.run(question)
    return answer

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator= "\n",
        chunk_size = 1000,
        chunk_overlap = 150,
        length_function = len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    document = FAISS.from_texts(texts = chunks, embedding = embeddings)
    #return the vector store
    return document

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.7, "max_length": 1500})

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return conversation_chain

def handle_user_input(user_question):

    response = st.session_state.conversation({'question' : user_question})
    st.session_state.chat_history = response['chat_history']


    for i,message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
