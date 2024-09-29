from services.vector_store import VectorStore
from fastapi.responses import FileResponse
from file_handler import FileHandler
from services import splitters
from services import loaders
from models import AImodels
import indicators as ind
import os
from services.llm import model
from services.prompt import prompt
from services.parsers import str_parser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


def audio_to_text(audio_file: bytes):
    audio_file_name = FileHandler().create_temp_file(audio_file, "wav")
    print(audio_file_name)
    if (type(audio_file_name) is not str) or ("Error" not in audio_file_name):
        with open("temp_audio.wav", "rb") as audio:
            text = AImodels().STT(audio)
        print(text)
        return text
    else:
        print("....", audio_file_name)
        return audio_file_name


def text_to_audio(text: str):
    audio_file_path = AImodels().TTS(text)
    if "Error" not in audio_file_path:
        # Return the audio file as a response
        if os.path.exists(audio_file_path):
            return FileResponse(audio_file_path, media_type='audio/mpeg', filename="speech.mp3")
        else:
            return f"{ind.error}Failed to generate speech"
    else:
        return f"{ind.error}Failed to generate speech"


def qa_from_url(url: str, query: str):
    print("Extracting data from URL...")
    full_page_content = loaders.web_loader(url)
    print("Splitting data...")
    chunked_content = splitters.chunker(full_page_content)
    print("Store Chunks in Vectore Store...")
    vector_db = VectorStore().store_docs(chunked_content)
    print("Get Retriever/Similar Chunks...")
    # similar_chunk = vector_db.similarity_search(query, k=1)
    retriever = vector_db.as_retriever()
    print("Splitting data...")
    setup_and_retrieval = RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    chain = setup_and_retrieval | prompt | model | str_parser
    result = chain.invoke(query)
    print("Cleaning Vector Store...")
    VectorStore().del_docs()
    # return result["content"]
    return result
    
