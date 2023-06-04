import streamlit as st
def sidebar():
    with st.sidebar:
        st.set_page_config(page_title="Chat Reader", page_icon="🎓", layout="wide")
        st.markdown('''
        # Chat Reader 
        Chat Reader allows you to ask questions about your documents and chat with multiple files at the same time.

        ## How this works 
        
        When you upload a document, it gets split into smaller sections and stored in a special kind of database called a vector index. This type of database allows for semantic search and retrieval, which means it can find related information even if the individual words aren't exact matches.
        
        When you ask a question, the model searches through these document sections using the vector index to find relevant information and ultimately provide an answer.
        
        ---
        ## How to use 🧐
        1. Upload your PDF files
        2. Click Submit before asking questions
        3. Ask your questions in the text box, and continue the chat for further questions
        4. You can ask it "What sources did you use?" to see the list of sources it used to answer your question.

        ## Are answer 100% accurate?
        The answers provided by the model are not guaranteed to be 100% accurate. While the model, powered by GPT-3, is a powerful language model, it can still make mistakes. Additionally, Chat Reader utilizes semantic search, which means it searches for the most relevant information within its knowledge base. However, it does not have access to the entire document and may not be able to find all the relevant information. This limitation is particularly evident for summary-type questions or questions that require a deep understanding of the document's context. It's important to independently verify information and consult reliable sources for critical or complex topics. 

        However, for most use cases, Chat Reader is very accurate and can answer most questions.

        ## Is your data safe?
        Yes, your data is safe. Chat Reader does not store your documents or questions. All uploaded data is deleted after you close the browser tab.

        ## About me
        Check out my [Web](https://mywebleo.com)
        ''')