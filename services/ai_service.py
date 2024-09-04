from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

# Get environment variables
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")


def get_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store():
        client = qdrant_client.QdrantClient(
           QDRANT_HOST,
            QDRANT_API_KEY
        ) 
        embeddings = OpenAIEmbeddings()
        vector_store = Qdrant(
            client=client, 
            collection_name=QDRANT_COLLECTION_NAME, 
            embeddings=embeddings,
        )
        
        return vector_store

class AIService:  
    @staticmethod
    def generate_output(user_question):
        try:
            # create vector store
            vector_store = get_vector_store()    
            # create chain 
            qa = RetrievalQA.from_chain_type(
                llm=OpenAI(),
                chain_type="stuff",
                retriever=vector_store.as_retriever()
            )
            answer = qa.run(user_question)
            return answer
        except Exception as e:
            print(f"Error generating output: {str(e)}")
            return None
    
    @staticmethod
    def add_documents(raw_text):
        try:
            texts = get_chunks(raw_text)
            vector_store = get_vector_store()
            vector_store.add_texts(texts)
            return True
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False 
         
