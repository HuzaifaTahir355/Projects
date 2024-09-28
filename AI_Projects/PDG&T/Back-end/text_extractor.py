from langchain_community.document_loaders import PyMuPDFLoader
from tika import parser

def extract_text_from_pdf(file_path):
    loader: PyMuPDFLoader = PyMuPDFLoader(file_path)
    data = loader.load()
    return data # return list of strings


def extract_text_from_other_files(file_path):
    parsed = parser.from_file(file_path)
    # print(parsed["metadata"]) #To get the meta data of the file
    return parsed["content"].strip() # To get the content of the file after remove extra spaces