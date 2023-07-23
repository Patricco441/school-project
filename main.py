import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from indexhtml import css,bot_template,user_template
from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf_docs):
 text = ""
 for pdf_doc in pdf_docs:
   pdf_reader = PdfReader(pdf_doc)
   for page in pdf_reader.pages:
    text+=page.extract_text()
    
   return text

def get_text_chunks(raw_text):
   text_splitter = CharacterTextSplitter(
     separator="\n",
     chunk_size=1000,
     chunk_overlap=200,
     length_function=len
   )
   chunks = text_splitter.split_text(raw_text)
   return chunks


def get_vectorstore(text_chunks):
  embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
  vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
  return vectorstore

def get_conversation_chain(vectorstore):
  llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

  memory=ConversationBufferMemory(memory_key='chat_history',return_messages=True)
  conversation_chain= ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory
    
  )
  return conversation_chain


def handle_userinput(user_question):
  if st.session_state.conversation is not None:
  
    response=st.session_state.conversation({'question':user_question})
 
    st.session_state.chat_history =response['chat_history']
    print(st.session_state.chat_history)
  
    for i,message in enumerate(st.session_state.chat_history):
      content = message.content  # Get the content of the message
      if isinstance(content, tuple):  # Check if the content is a tuple
        content = ' '.join(content)  # Join the elements of the tuple into a single string
      if i % 2 == 0:
        st.write(user_template.replace("{{MSG}}", content), unsafe_allow_html=True)
      else:
        st.write(bot_template.replace("{{MSG}}", content), unsafe_allow_html=True)
    
  else:
        # Handle the case where st.session_state.conversation is None
        # e.g., display a message asking the user to upload a PDF and click "Process"
        st.write("Please upload a PDF and click 'Process' before asking a question.")



def main():
   load_dotenv()
   st.set_page_config(page_title="Chat with PDF 💾" ) 
   st.write(css,unsafe_allow_html=True) 

   if "conversation" not in st.session_state:
     st.session_state.conversation = None

   if "chat_history" not in st.session_state:
       st.session_state.chat_history = None
    

   st.header("Chat with PDF 💾 ")
   user_question= st.text_input("Ask your question here")
   if user_question:
     handle_userinput(user_question)
 
   # st.write(user_template.replace("{{MSG}}","hello bot"),unsafe_allow_html=True)
   # st.write(bot_template.replace("{{MSG}}","hello human"),unsafe_allow_html=True)
   
   with st.sidebar:
       st.subheader("Your PDFs")
       pdf_docs= st.file_uploader(" Drag and drop your PDF here. Then click on 'Process'", type=["PDF"], accept_multiple_files=True)
       if st.button("Process"):
        with st.spinner("Processing..."):
          raw_text = get_pdf_text(pdf_docs)
          st.write(raw_text)

          text_chunks=get_text_chunks(raw_text)
          st.write(text_chunks)
          vectorstore=get_vectorstore(text_chunks)

          st.session_state.conversation = get_conversation_chain(vectorstore)
          st.success("Done! Now ask your question in the text box on the left.")

if __name__ == "__main__":
    main() 