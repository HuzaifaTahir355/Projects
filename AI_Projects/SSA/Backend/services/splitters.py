from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunker(text: str):
    size_of_chunk = 700
    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=size_of_chunk,
        chunk_overlap=size_of_chunk*10/100,
        length_function=len
    )
    return text_splitter.split_documents(text)