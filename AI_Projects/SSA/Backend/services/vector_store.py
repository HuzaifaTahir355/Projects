from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, Filter
from env import Env
from services import embedder


class VectorStore:
    def __init__(self) -> None:
        self.client = QdrantClient(url=Env.get("QDRANT_URL"), 
                                   api_key=Env.get("QDRANT_API_KEY"))


    def store_docs(self, data):
        qdrant = QdrantVectorStore.from_documents(
            # QdrantClient=self.client,
            documents=data,
            embedding=embedder.embedding_model,
            url=Env.get("QDRANT_URL"),
            prefer_grpc=True,
            api_key=Env.get("QDRANT_API_KEY"),
            collection_name=Env.get("QDRANT_COLLECTION_NAME"),
        )
        return qdrant


    def del_docs(self):
        self.client.delete(
            collection_name=Env.get("QDRANT_COLLECTION_NAME"),
            points_selector=Filter(must=[])  # Empty 'must' means no conditions, selects all points
            )
        print(f"All points deleted from collection {Env.get('QDRANT_COLLECTION_NAME')}.") 