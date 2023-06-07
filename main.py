import streamlit as st
from dotenv import load_dotenv 
from components.sidebar import sidebar
from html_css import css, bot_template, user_template

from utils import (
    get_pdf_text,
    get_docx_text,
    get_txt_text,
    get_csv_answer,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
    handle_user_input
)

sidebar()

def main():
    load_dotenv()
    st.write(css, unsafe_allow_html=True)
    st.title("Chat with multiples files 🎓")
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.button("Analyze data with CSV files")
    docs = st.file_uploader("Upload your files", type = ["pdf","docx", "txt", "csv"], accept_multiple_files=True)
    
    csv_key = 0
 
    if docs is not None and st.button("Submit"):
        with st.spinner("Processing..."):
            #get the pdf text
            raw_text = ""
            for doc in docs:
                if doc.name.endswith(".csv"):
                    csv_key = 1
                    break
                elif doc.name.endswith(".pdf"):
                    raw_text += get_pdf_text([doc])
                elif doc.name.endswith(".docx"):
                    raw_text += get_docx_text(doc)
                elif doc.name.endswith(".txt"):
                    raw_text += get_txt_text(doc)
            if csv_key == 0:
                #split text into chunks
                chunks = get_text_chunks(raw_text)
                
                #create embeddings and vector index
                vectorstore = get_vectorstore(chunks)

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)


    user_question = st.text_input("Enter your question about the files:  💬")

    if user_question and (csv_key == 0):
        handle_user_input(user_question)
    # elif user_question and (csv_key == 1):
    #     answer = get_csv_answer(docs, user_question)
    #     st.write(answer)
    #     st.session_state.chat_history = None
    #     st.session_state.conversation = None



if __name__ == '__main__':
    main()