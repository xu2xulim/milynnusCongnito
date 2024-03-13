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
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 💬")

    if "authentication_status" in st.session_state:
        if st.session_state['authentication_status']:
            pass
        else:
            st.switch_page("streamlit_app.py")
    else:
        st.switch_page("streamlit_app.py")
    
    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if st.button("Return 🏠"):
        st.switch_page("streamlit_app.py")
    
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
      user_question = st.text_input("Ask a question about your PDF:")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)
        
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run({"input_documents" : docs, "question" : user_question})
          print(cb)

        st.session_state.chat_history=[]   
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
    

if __name__ == '__main__':
    main()