from fastapi import APIRouter, status, Body, UploadFile, File
import interactor
from pydantic import BaseModel

router = APIRouter(
    tags=["Routes"]
)

class TextToSpeechRequest(BaseModel):
    text: str

class SpeechToTextRequest(BaseModel):
    audio_file: UploadFile = File(...)

class QAFromUrlRequest(BaseModel):
    url: str
    query: str

# @router.get('/get-uploaded-files', status_code=status.HTTP_200_OK)
# def get_files():
#     return files_mgmt_interactor.get_uploaded_files()


@router.post("/audio-to-text", status_code=status.HTTP_201_CREATED)
# def audio_to_text(request: SpeechToTextRequest):
def audio_to_text(audio_file: UploadFile = File(...)):
    print("Audio File Received!")
    return interactor.audio_to_text(audio_file)


@router.post("/qa-from-url", status_code=status.HTTP_200_OK)
def qa_from_url(request: QAFromUrlRequest):
    return interactor.qa_from_url(request.url, request.query)


@router.post("/text-to-audio", status_code=status.HTTP_201_CREATED)
def audio_to_text(request: TextToSpeechRequest):
    print("Text Received!")
    return interactor.text_to_audio(request.text)


# @router.delete("/delete-all-files", status_code=status.HTTP_204_NO_CONTENT)
# def delete_all_files():
#     return files_mgmt_interactor.delete_all_files_data()