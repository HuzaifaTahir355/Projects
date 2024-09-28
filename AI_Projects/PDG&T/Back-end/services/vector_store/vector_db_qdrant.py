from constants import VECTOR_DB_INDEX_NAME
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore, Qdrant
from env import Env
from qdrant_client.http.models import VectorParams, Distance, Filter, FieldCondition, MatchValue
from langchain_community.vectorstores import Qdrant
from services.db.settings import DBHandlerSettings

class QdrantDB:
    def __init__(self):
        self.client = QdrantClient(url = Env.get('QDRANT_URL'),
                                   api_key = Env.get('QDRANT_API_KEY'))


    def create_index(self):
        collection_names = [collection.name for collection in self.client.get_collections().collections]
        embedding_model_dimensions = DBHandlerSettings().get_embedding_model_dimension()
        if VECTOR_DB_INDEX_NAME not in collection_names:
            print("Creating New Collection....")
            self.client.create_collection(collection_name=VECTOR_DB_INDEX_NAME, 
                                          vectors_config=VectorParams(size=embedding_model_dimensions, 
                                                                      distance=Distance.COSINE))
        return VECTOR_DB_INDEX_NAME


    def initialize_vector_db(self, index, embedding_model):
        vector_db = QdrantVectorStore(client=self.client, 
                                      embedding=embedding_model, 
                                      collection_name=index)
        return vector_db

    
    def get_related_chunks(self, files_data, vector_store, embeddings):
        retrieved_chunks: list = []
        vector_store = Qdrant(client = self.client,
                              embeddings = embeddings,
                              collection_name = VECTOR_DB_INDEX_NAME,
                              content_payload_key  = 'unique_key',
                              metadata_payload_key = 'metadata',
                              )
        for file in files_data:
            # result = vector_store.similarity_search(query="what is the Product name and Product description", 
            #                                         k = 1,
            #                                         filter = Filter(should=[
            #                                             FieldCondition(
            #                                                 key="unique_key",
            #                                                 match=MatchValue(value=file[0])
            #                                                 )]
            #                                             )
            #                                         )
            retriever = vector_store.as_retriever(search_kwargs={"k": 1,
                                                              "filter": Filter(should=[
                                                                            FieldCondition(
                                                                                key="unique_key",
                                                                                match=MatchValue(value=file[0])
                                                                                )]
                                                                            )}
                                                                            )
            
            result = retriever.invoke("Product description")
            print("--->", result)
            if result:
                retrieved_chunks.append((result[0].page_content,))
        print(retrieved_chunks)
        return retrieved_chunks


    def delete_index(self):
        self.client.delete_collection(VECTOR_DB_INDEX_NAME)
    

    def delete_all_documents(self):
        print(self.client.delete(collection_name=VECTOR_DB_INDEX_NAME, points_selector=Filter()))  # Empty filter matches all vectors