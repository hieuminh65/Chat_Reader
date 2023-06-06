import streamlit as st
def sidebar():
    with st.sidebar:
        st.set_page_config(page_title="Chat Reader", page_icon="🎓", layout="wide")
        st.markdown('''
        # Chat Reader 
        Chat Reader allows you to ask questions about your documents and chat with multiple files at the same time.

        ---
        ## How to use 🧐
        1. Upload your files. Supported formats are PDF, DOCX, and TXT.
        2. **Click Submit before asking questions**
        3. Ask your questions in the text box, and continue the chat for further questions

        ## How to optimize the results :brain:
        Ask questions like 'Where did you get this information from?', 'What sources did you use?', etc, to see the list of sources it used to answer your question.
        ## Are answer 100% accurate?
        The answers provided by the model are not guaranteed to be 100% accurate. While the model, powered by GPT-3, is a powerful language model, it can still make mistakes. 

        However, for most use cases, Chat Reader is very accurate and can answer most questions.

        ## Is your data safe?
        The data is safe. All uploaded data is deleted after you close the browser tab.

        ## About me
        Check out my [Web](https://mywebleo.com)
        ''')