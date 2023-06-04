import streamlit as st
from dotenv import load_dotenv 
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from html_css import css, bot_template, user_template

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return conversation_chain

def get_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    document = FAISS.from_texts(texts = chunks, embedding = embeddings)
    #return the vector store
    return document

def get_pdf_text(pdf_docs):
    text = ""
    for pdf_doc in pdf_docs:
        pdf_reader = PdfReader(pdf_doc)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator= "\n",
        chunk_size = 1000,
        chunk_overlap = 150,
        length_function = len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def handle_user_input(user_question):
    response = st.session_state.conversation({'question' : user_question})
    st.write(response)

with st.sidebar:
    st.set_page_config(page_title="Chat Reader")
    st.markdown('''
    ## How this works
    When you upload a document, it gets split into smaller sections and stored in a special kind of database called a vector index. This type of database allows for semantic search and retrieval, which means it can find related information even if the individual words aren't exact matches. 

    When you ask a question, the model searches through these document sections using the vector index to find relevant information and ultimately provide an answer.

    ## About me
    Check out my [Web](https://mywebleo.com)
    ''')


def main():
    load_dotenv()
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = None

    st.title("Chat Reader with multiples files")
    st.header("Chat with multiples files")

    pdf_docs = st.file_uploader("Upload your PDF files at once", type = ["pdf"], accept_multiple_files=True)
    st.button("Submit")
    if st.button:
        with st.spinner("Processing..."):
            #get the pdf text
            raw_text = get_pdf_text(pdf_docs)

            #split text into chunks
            chunks = get_text_chunks(raw_text)
            
            #create embeddings and vector index
            vectorstore=get_vectorstore(chunks)

            #create conversation chain
            st.session_state.conversation = get_conversation_chain(vectorstore)

    st.session_state.conversation

    user_question = st.text_input("Enter your question about the files: ")
    if user_question:
        handle_user_input(user_question)
    st.write(user_template.replace("{{MSG}}", "Hello, I have a question about the files."), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello"), unsafe_allow_html=True)


if __name__ == '__main__':
    main()