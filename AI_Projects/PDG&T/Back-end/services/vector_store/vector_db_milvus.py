from langchain_milvus import Milvus
from pymilvus import MilvusClient


class MilvusDB:
    def __init__(self) -> None:
        self.uri = "milvus_example.db"
        self.client = MilvusClient(uri=self.uri)


    def create_index(self):
        pass


    def initialize_vector_db(self, index, embedding_model):
        vector_store = Milvus(
            embedding_function=embedding_model,
            connection_args={"uri": self.uri},
            auto_id=True
        )
        return vector_store


    def get_related_chunks(self, files_data, vector_store):
        retrieved_chunks: list = []
        for file in files_data:
            retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1})
            result = retriever.invoke("what is the Product name and Product description", filter = {'unique_key': file[0]})
            if result:
                retrieved_chunks.append((result[0].page_content,))
        return retrieved_chunks
    

    def delete_all_documents(self, collection_name: str = "LangChainCollection"):
        if self.client.has_collection(collection_name=collection_name):
            self.client.drop_collection(collection_name=collection_name)
            return f"{collection_name} - Collection deleted Successfully"
        return f"Collection Not found named {collection_name}"