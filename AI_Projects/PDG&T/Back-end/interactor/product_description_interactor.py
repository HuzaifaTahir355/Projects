from text_extractor import extract_text_from_pdf, extract_text_from_other_files
from llm import get_llm, get_response_from_llm, verify_translated_response
from services.splitters import Splitter
from services.unique_id import UniqueIdGenerator
from services.embedder import Embedder
from services.file_handler import FileHandler
from services.db.product_description import DBHandlerPD
from services.db.settings import DBHandlerSettings
import json
import constants as c


def get_available_llms():
    if c.LLMS:
        return c.LLMS
    else:
        return False


def generate_product_description(languages: list[str]):
    complete_response: list[dict] = []
    data = DBHandlerPD().get_product_description_data_from_db()
    selected_llm: str = DBHandlerSettings().get_setted_llm()
    is_image_required: bool = False

    if data:
        model = get_llm(selected_llm)
        for row_data in data:
            translated_response = json.loads(get_response_from_llm(row_data, languages, model))
            if "Not Found" not in translated_response:
                if is_image_required:
                    pass
            
                complete_response = complete_response + translated_response
    return complete_response


        





























# def get_chunks_from_extracted_text(extracted_text):
#     temp_content = ""
#     for text_chunk in extracted_text:
#         temp_content += text_chunk.page_content
#     return temp_content
    

async def process_files(uploaded_files, languages: list[str]):
    content: str = FileHandler.get_text(uploaded_files)
    chunked_content: list = Splitter.get_text_chunks(content)
    keys : list[str] = UniqueIdGenerator.get_unique_id(len(chunked_content))
    embedding_model = Embedder.get_embedding_model()

    # index = PineconeDB().create_index("pdg-index")
    # vector_store = PineconeDB.initialize_vector_db(index, embedding_model)
    # vector_store.add_documents(documents=chunked_content, ids=keys)
    # retriever = vector_store.as_retriever()
    # print(retriever.invoke("what is the name and description of Product"))


    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableParallel, RunnablePassthrough
    model = ChatOpenAI(model="gpt-4o-mini")

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()

    # setup_and_retrieval = RunnableParallel(
    #     {"context": retriever, "question": RunnablePassthrough()}
    # )
    # chain = setup_and_retrieval | prompt | model | output_parser

    # print(chain.invoke("what is the name and description of Product?"))






    # print(len(chunked_content))
    # print(chunked_content)
    # print(keys)
    # return content
    # content: str = ""
    # for file in uploaded_files:
    #     if "pdf" in file.headers["content-type"]:
    #         with open(file.filename, "wb") as f:
    #             f.write(await file.read())
    #         extracted_text: list = extract_text_from_pdf(file.filename)
    #         content += get_chunks_from_extracted_text(extracted_text)
    #         os.remove(file.filename)
    #     else:
    #         if "image" not in file.headers["content-type"]:
    #             with open(file.filename, "wb") as f:
    #                 f.write(await file.read())
    #             extracted_text: any = extract_text_from_other_files(file.filename)
    #             content += extracted_text
    #             os.remove(file.filename)
"""
    if content:
        complete_response: list[dict] = []
        # create Chunks
        # chunked_content: list[str] = chunk_creator(content)
        # get llm response on each chunk and add it in complete_response list 
        for single_chunk in chunked_content:
            translated_response: list = json.loads(get_response_from_llm(single_chunk, languages))
            if "Not Found" not in translated_response:
                complete_response = complete_response + translated_response

        if complete_response:
            for dictionary_of_products in complete_response:
                description_in_english: str = dictionary_of_products['description']['English']
                for language in languages:
                    translated_language_description: str = dictionary_of_products['description'][language]
                    # Dual Verification of translation
                    # TDOD: use async batch to concurrently
                    verified_translated_response: str = verify_translated_response(description_in_english, language, translated_language_description)
                    if str.lower(verified_translated_response) != "verified":
                        dictionary_of_products['description'][language] = verified_translated_response

        return complete_response
    else:
        return "Error_File not supported"
"""