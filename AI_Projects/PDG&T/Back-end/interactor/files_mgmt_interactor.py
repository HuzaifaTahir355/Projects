from services.data_formatter import DataFormatter
from services.file_handler import FileHandler
from services.db.db import DB
from fastapi import UploadFile
from services.vector_db_handler import VectorDB
import constants as c
from services.db.product_description import DBHandlerPD
from services.db.files_mgmt import DBHandlerFM
from services.splitters import Splitter
from services.db.settings import DBHandlerSettings


def get_default_chunk_size():
    return c.DEFAULT_CHUNK_SIZE


def get_available_embedding_models(chunk_size: int):
    embedding_models = c.EMBEDDING_MODEL_WITH_DIMENSIONS
    if embedding_models:
        return [model["model"] for model in embedding_models if model["dimension"] >= chunk_size]
    else:
        return False


def get_available_vector_stores():
    if c.VECTOR_STORES:
        return c.VECTOR_STORES
    else:
        return False


def get_uploaded_files():
    table_columns, db_data = DBHandlerFM().get_data_from_table(column_names=True)
    if db_data:
        formatted_data =  DataFormatter().db_response_to_list_of_dicts(table_columns, db_data)
        return formatted_data
    else:
        return db_data


def file_uploader(files: list[UploadFile]):
    db_response     :str | None = None
    chunk_size      :int  = DBHandlerSettings().get_setted_chunk_size()
    embedding_model :str  = DBHandlerSettings().get_setted_embedding_model()
    vector_store    :str  = DBHandlerSettings().get_setted_vector_store_name()
    data_to_store_in_db, rejected_files_name = FileHandler().prepare_files_for_storage(files, vector_store)

    if data_to_store_in_db:
        ("Storing Data in DB...")
        db_response = DBHandlerFM().store_data_in_db(data_to_store_in_db)
        if db_response and "Success" in db_response:
            print("Creating Documents...")
            create_document_from_files: list = FileHandler().read_files_and_prepare_documents(data_to_store_in_db)
            print("Splitting Chunks...")
            chunked_content: list = Splitter.get_chunked_documents(create_document_from_files, 
                                                                   chunk_size)
            print("Storing Chunks in Vector Store...")
            data_ready_for_qa = VectorDB().store_document_in_vector_db_and_retrieve_relevent_chunks(embedding_model, 
                                                                                                    chunked_content, 
                                                                                                    data_to_store_in_db, 
                                                                                                    vector_store)
            print("Storing PD Data in DB...")
            print(DBHandlerPD().store_data_in_db(data_ready_for_qa))

    rejected_files_message = f"These files are already exists - {rejected_files_name}"
    return db_response, rejected_files_message


def delete_all_files_data():
    try:
        #  delete index from vector DB
        VectorDB().delete_documents()
        # Delete chunks from DB
        DBHandlerPD().delete_all_data()
        # delete files from DB
        DBHandlerFM().delete_all_data()
        # delete files from local
        FileHandler().remove_all_files()
        
        return "Deleted Successfully"
    except Exception as e:
        return f"Error occured while deleting files - {e}"


