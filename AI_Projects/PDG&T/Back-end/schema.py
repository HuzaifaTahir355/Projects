from pydantic import BaseModel
from fastapi import UploadFile

class ProductDescriptionRequest(BaseModel):
    languages        : list[str]

class SettingsRequest(BaseModel):
    chunk_size       : int
    embedding_model  : str
    vector_store     : str
    is_image_required: bool
    selected_llm     : str
    