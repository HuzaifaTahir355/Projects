from langchain_community.document_loaders import WebBaseLoader

def web_loader(url: str):
    loader: WebBaseLoader = WebBaseLoader(url)
    docs = loader.load()
    return docs