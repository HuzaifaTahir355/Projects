from services.data_formatter import DataFormatter
import constants as c
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


def get_saved_settings():
    table_columns, db_data = DBHandlerSettings().get_settings_data_from_db(is_column_name_required=True)
    if db_data:
        formatted_data =  DataFormatter().db_response_to_list_of_dicts(table_columns, db_data)
        return formatted_data
    else:
        return db_data


def save_settings(chunk_size       : int,
                  embedding_model  : str,
                  vector_store     : str,
                  is_image_required: bool,
                  selected_llm     : str):
    
    embedding_model_dimension: int = 1024
    embedding_models = c.EMBEDDING_MODEL_WITH_DIMENSIONS
    if embedding_models:
        for model in embedding_models:
            if model["model"] == embedding_model:
                embedding_model_dimension = model["dimension"]
                break
        print(embedding_model_dimension)
        data: list = [(chunk_size, embedding_model, embedding_model_dimension, vector_store, is_image_required, selected_llm)]
        return DBHandlerSettings().save_settings_in_db(data)

