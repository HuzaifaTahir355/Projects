from fastapi import APIRouter, status, UploadFile, File
from interactor import files_mgmt_interactor

router = APIRouter(
    tags=["Files Management"]
)


@router.get('/get-uploaded-files', status_code=status.HTTP_200_OK)
def get_files():
    return files_mgmt_interactor.get_uploaded_files()


@router.post("/upload-files", status_code=status.HTTP_201_CREATED)
def files_upload(files: list[UploadFile] = File(...)):  # Expecting a list of files
    print("Files Received!")
    return files_mgmt_interactor.file_uploader(files)


@router.delete("/delete-all-files", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_files():
    return files_mgmt_interactor.delete_all_files_data()