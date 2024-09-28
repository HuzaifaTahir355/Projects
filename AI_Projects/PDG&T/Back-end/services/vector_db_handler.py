from services.vector_store.vector_db_pinecone import PineconeDB
from services.vector_store.vector_db_qdrant import QdrantDB
from services.vector_store.vector_db_milvus import MilvusDB
from services.embedder import Embedder
import constants as c
import time

class VectorDB:
    def __init__(self):
        self.vector_db = ""


    def store_document_in_vector_db_and_retrieve_relevent_chunks(self, embedding_model, chunked_content, files_data, vector_store):
        self.string_to_class_mapper(vector_store)
        index = self.create_index()
        embedding_model = Embedder().get_embedding_model(embedding_model)
        vector_store = self.initialize_vector_db(index, embedding_model)
        vector_store.add_documents(documents=chunked_content)
        relevent_chunks = self.get_relevent_chunks(files_data, vector_store)
        return relevent_chunks


    def get_relevent_chunks(self, files_data, vector_store):
        retrieved_chunks = self.vector_db.get_related_chunks(files_data, vector_store)
        # if retrieved_chunks:
        if len(files_data) > len(retrieved_chunks):
            print(".....Try again to get chunks......")
            while len(files_data) > len(retrieved_chunks):
                print("<--!!-->", len(files_data), len(retrieved_chunks))
                retrieved_chunks = self.vector_db.get_related_chunks(files_data, vector_store)
        return retrieved_chunks


    def reset_retrieved_chunks(self):
        self.retrieved_chunks.clear()
        if not self.retrieved_chunks:
            return True
        else:
            return False


    def create_index(self):
        return self.vector_db.create_index()
        

    def delete_index(self, vector_store: str):
        self.string_to_class_mapper(vector_store)
        return self.vector_db.delete_index()


    def delete_documents(self):
        try:
            for vector_store in c.VECTOR_STORES:
                self.string_to_class_mapper(vector_store)
                self.vector_db.delete_all_documents()
            return "Deleted Successfully"
        except Exception as e:
            print(e)


    def initialize_vector_db(self, index, embedding_model):
        return self.vector_db.initialize_vector_db(index, embedding_model)
    

    def string_to_class_mapper(self, user_selected_vectordb_name):
        if user_selected_vectordb_name == "Pinecone":
            self.vector_db = PineconeDB()
        elif user_selected_vectordb_name == "Milvus":
            self.vector_db = MilvusDB()
        elif user_selected_vectordb_name == "Qdrant":
            self.vector_db = QdrantDB()


