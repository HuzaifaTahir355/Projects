from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.documentor import Documentor

class Splitter:
    def get_chunked_documents(list_of_documents: list, chunk_size: int):
        splitter = Splitter()
        return splitter.__recursive_splitter(list_of_documents, chunk_size)
    
    def __recursive_splitter(self, list_of_documents: list, chunk_size: int):
        text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size*(10/100)), # 10% of chunk size
            length_function=len,
        )
        return text_splitter.split_documents(list_of_documents)

    