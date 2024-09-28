from langchain_core.documents import Document

class Documentor:
    def create_document(text: str, 
                        metadata: None | dict = None):
        if metadata:
            return Document(
                page_content = text, 
                metadata = metadata
            )
        else:
            return Document(
                page_content=text
            )
    