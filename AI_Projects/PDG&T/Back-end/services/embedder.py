from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

class Embedder:
    def get_embedding_model(self, user_selection: str):
        if user_selection == "BAAI/bge-large-en-v1.5":
            return HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-en-v1.5")
        elif user_selection == "sentence-transformers/all-mpnet-base-v2":
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    