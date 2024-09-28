from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import faiss


class FaissDB:
    def create_index(self):
        index = faiss.IndexFlatL2(1024)
        return index 
    

    def initialize_vector_db(self, index, embedding_model):
        vector_store = FAISS(embedding_function=embedding_model,
                             index=index,
                             docstore=InMemoryDocstore(),
                             index_to_docstore_id={}
                             )
        return vector_store
    

    def delete_index(self, index_name: str):
        self.pc.delete_index(index_name)


    def delete_all_documents(self, vector_store):
        return vector_store.delete(delete_all=True)
