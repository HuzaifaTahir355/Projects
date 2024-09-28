from fastapi import APIRouter, status
from interactor import settings_interactor
from schema import SettingsRequest

router = APIRouter(
    tags=["Settings"]
)


@router.get('/get-default-chunk-size', status_code=status.HTTP_200_OK)
def default_chunk_size():
    return settings_interactor.get_default_chunk_size()


@router.get('/get-available-embedding-models/{chunk_size}', status_code=status.HTTP_200_OK)
def available_embedding_models(chunk_size: int):
    return settings_interactor.get_available_embedding_models(chunk_size)


@router.get('/get-available-vector-stores', status_code=status.HTTP_200_OK)
def available_vector_stores():
    return settings_interactor.get_available_vector_stores()


@router.get('/get-saved-settings', status_code=status.HTTP_200_OK)
def get_saved_settings():
    return settings_interactor.get_saved_settings()


@router.post("/save-settings", status_code=status.HTTP_201_CREATED)
def save_settings(request: SettingsRequest):
    return settings_interactor.save_settings(request.chunk_size,
                                             request.embedding_model,
                                             request.vector_store,
                                             request.is_image_required,
                                             request.selected_llm)

