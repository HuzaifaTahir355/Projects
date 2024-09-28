from langchain_community.document_loaders import PyMuPDFLoader
from services.directory_operations import DirectoryOperations
from services.unique_id import UniqueIdGenerator
from services.documentor import Documentor
from raise_exception import RaiseException
from constants import NOT_ALLOWED_FORMATS
from services.date_time import Datetime
from fastapi import UploadFile
from tika import parser
import os

class FileHandler:
    def __init__(self):
        self.file_storage_path: str = os.getcwd() + "/file_storage/"


    def read_files_and_prepare_documents(self, files: list[tuple]):
        list_of_documents: list = []
        for file in files:
            file_extension = file[2]
            if file_extension == "pdf":
                documents = self.__get_pdf_data(file[4])
                for doc in documents:
                    doc.metadata["unique_key"] = file[0]
                    list_of_documents.append(doc)
            else:
                content = self.__get_other_formats_data(file[4])
                if content:
                    document = Documentor.create_document(content, metadata={"unique_key": file[0], "source": file[1]})
                    list_of_documents.append(document)   
        return list_of_documents


    def __get_file_extension(self, file: UploadFile):
        return file.filename.split(".")[-1]

   
    def __get_file_size(self, file: UploadFile):
        return file.size


    def __validate_file_type(self, filetype):
        if filetype in NOT_ALLOWED_FORMATS:
            RaiseException.invalid_file_format()


    def __save_file_locally(self, file: UploadFile):
        try:
            with open(self.file_storage_path + file.filename, "wb") as f:
                f.write(file.file.read())
            return self.file_storage_path + file.filename
        except Exception as e:
            return False


    def remove_single_file(self, filename: None | str = None):
        try:
            if filename:
                os.remove(self.file_storage_path + filename)
        except Exception as e:
            print(e)


    def remove_all_files(self,
                         files: list[str] = os.listdir('file_storage')):
        for file in files:
            self.remove_single_file(file)


    def __get_pdf_data(self, filepath: str):
        try:
            loader = PyMuPDFLoader(filepath, extract_images=True)
            data = loader.load()
            return data
        except Exception as e:
            RaiseException.data_extraction_error(e)

 
    def __get_other_formats_data(self, filepath: str):
        try:
            parsed = parser.from_file(filepath)
            if parsed:
                return parsed['content']
            else:
                return ""
        except Exception as e:
            RaiseException.data_extraction_error(e)


    def prepare_files_for_storage(self, files: list[UploadFile], vector_store: str):
        existing_files: list[str] = DirectoryOperations().get_list_of_files_or_folders('file_storage')
        data_to_store_in_db: list = []
        rejected_files_name: list = []
        print("saving files locally...")
        for file in files:
            file_name = file.filename
            if file_name not in existing_files:
                file_unique_key = UniqueIdGenerator.get_unique_id(1)
                file_extension = self.__get_file_extension(file)
                file_size = self.__get_file_size(file)
                file_local_path = self.__save_file_locally(file)
                if not file_local_path:
                    rejected_files_name.append(file_name)
                    continue
                current_date = Datetime.get_current_date()
                # append that data in final list
                data_to_store_in_db.append((file_unique_key, 
                                            file_name, 
                                            file_extension, 
                                            file_size, 
                                            file_local_path, 
                                            current_date, 
                                            vector_store))
            else:
                rejected_files_name.append(file_name)

        return data_to_store_in_db, rejected_files_name