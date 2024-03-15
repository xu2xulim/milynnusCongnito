from dotenv import load_dotenv
import streamlit as st

from langchain_core.messages import AIMessage, HumanMessage
#from langchain_community.document_loaders import WebBaseLoader
#from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI #ChatOpenAI
#from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
#from langchain.chains import create_history_aware_retriever, create_retrieval_chain
#from langchain.chains.combine_documents import create_stuff_documents_chain


from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
#from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
#from langchain.llms import OpenAI
#from langchain_community.llms import OpenAI
#from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDF")
    st.header("Chat your PDF 💬")

    if "authenticated" in st.session_state:
        if st.session_state['authenticated']:
            pass
        else:
            st.switch_page("streamlit_app.py")
    else:
        st.switch_page("streamlit_app.py")
    
    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if st.button("Return 🏠"):
        st.switch_page("pages/home.py")
    
    # extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
      
        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
      
        # show user input
        #user_question = st.text_input("Chat with PDF:")

        col1, col2, col3, col4 = st.columns(4)
            
        if "chat_history" not in st.session_state:
            user_question = None
            with col1: 
                if st.button('Top 10 Key Points'):
                    user_question = "Give me the 10 keys points"
                    st.session_state.starter = True
                    
            with col2:
                if st.button('100 word summary'):
                    user_question = "Create a 100 word summary"
                    st.session_state.starter = True

            with col3:
                if st.button('500 word summary'):
                    user_question = "Create a 500 word summary"
                    st.session_state.starter = True

            with col4:
                if st.button('1000 word summary'):
                    user_question = "Create a 1000 word summary"
                    st.session_state.starter = True

            if user_question != None:
                st.session_state.chat_history = [
                    AIMessage(content="Hello, I am a SavvyAI. How can I help you?"),]     
        else:
            user_question = st.chat_input("Type your message here...")
      


        if user_question:
            docs = knowledge_base.similarity_search(user_question)
        
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run({"input_documents" : docs, "question" : user_question})
                print(cb)
           
            st.session_state.chat_history.append(HumanMessage(content=user_question))
            st.session_state.chat_history.append(AIMessage(content=response))
        
        if "chat_history" in st.session_state:
            
            for message in st.session_state.chat_history:
                if isinstance(message, AIMessage):
                    with st.chat_message("AI"):
                        st.write(message.content)
                elif isinstance(message, HumanMessage):
                    with st.chat_message("Human"):
                        st.write(message.content)
            
            if "starter" in st.session_state:
                if st.session_state.starter:
                    st.session_state.starter = False
                    st.rerun()
    

if __name__ == '__main__':
    main()