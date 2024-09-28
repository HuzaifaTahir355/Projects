from services.db.settings import DBHandlerSettings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from constants import VECTOR_DB_INDEX_NAME
from env import Env
import time



class PineconeDB:
    def __init__(self):
        self.pc = Pinecone(api_key=Env.get('PINECONE_API_KEY'))
        self.existing_indexes = [index_info['name'] for index_info in self.pc.list_indexes()]


    def create_index(self):
        embedding_model_dimensions = DBHandlerSettings().get_embedding_model_dimension()
        index_name: str = VECTOR_DB_INDEX_NAME
        if index_name not in self.existing_indexes:
            self.pc.create_index(
                name=index_name,
                dimension=embedding_model_dimensions,
                metric="cosine",
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
        
            while not self.pc.describe_index(index_name).status["ready"]:
                time.sleep(1)
        return self.pc.Index(index_name) 


    def get_related_chunks(self, files_data, vector_store):
        retrieved_chunks: list = []
        for file in files_data:
            retriever = vector_store.as_retriever(search_kwargs={'k': 1, 'filter': {'unique_key': file[0]}})
            result = retriever.invoke("what is the Product name and Product description")
            if result:
                retrieved_chunks.append((result[0].page_content,))
        return retrieved_chunks


    def initialize_vector_db(self, index, embedding_model):
        vector_db = PineconeVectorStore(index=index, embedding=embedding_model)
        return vector_db


    def delete_index(self):
        self.pc.delete_index(VECTOR_DB_INDEX_NAME)
    

    def delete_all_documents(self):
        try:
            return self.pc.delete_index(VECTOR_DB_INDEX_NAME)
        except Exception as e:
            print(e)