import requests
import base64

class ApiCalls:
    def __init__(self):
        # set base URL
        self.baseurl: str = "http://127.0.0.1:8000/"


    def __get_requester(self, url: str):
        try:
            self.response: requests = requests.get(url=url)
            # if response is successful
            if self.response.status_code == 200:
                return self.response.json()
            else:
                print(self.response.status_code)
        except Exception as e:
            print(e)


    def text_from_speech(self, audio_bytes: bytes):
        self.url: str = self.baseurl + "audio-to-text"
        # Assuming you want to send the audio bytes with a filename and content type
        self.files = {"audio_file": audio_bytes}
        try:
            self.response: requests = requests.post(url=self.url, files=self.files)
            if self.response.status_code == 201:
                return self.response.json()
        except Exception as e:
            print(e)


    def qa_from_url(self, url: str, query: str):
        self.url: str = self.baseurl + "qa-from-url"
        self.data = {
            "url": url,
            "query": query
            }
        try:
            self.response: requests = requests.post(url=self.url, json=self.data)

            if self.response.status_code == 200:
                return self.response.json()
        except Exception as e:
            print(e)


    def text_to_speech(self, text: str):
        self.url: str = self.baseurl + "text-to-audio"
        # Assuming you want to send the audio bytes with a filename and content type
        self.data = {"text": text}
        try:
            self.response: requests = requests.post(url=self.url, json=self.data)
            print(self.response.status_code)
            if self.response.status_code == 200:
                # Get the audio file from FastAPI and play it
                audio_data = self.response.content
                return audio_data
        except Exception as e:
            print(e)
        


    def get_default_chunk_size(self):
        self.url: str = self.baseurl + f"get-default-chunk-size"
        return self.__get_requester(self.url)


    def get_available_embedding_models(self, chunk_size: int):
        self.url: str = self.baseurl + f"get-available-embedding-models/{chunk_size}"
        response: any | None = self.__get_requester(self.url)
        if response:
            return response
        else:
            return []


    def get_available_vector_stores(self):
        self.url: str = self.baseurl + "get-available-vector-stores"
        response: any | None = self.__get_requester(self.url)
        if response:
            return response
        else:
            return []


    def get_available_llms(self):
        self.url: str = self.baseurl + "get-available-llms"
        response: any | None = self.__get_requester(self.url)
        if response:
            return response
        else:
            return []
        

    def upload_files(self, uploaded_files: list):
        self.url: str = self.baseurl + "upload-files"
        self.files_payload: list = [("files", (file.name, file, file.type)) for file in uploaded_files]
        try:
            self.response: requests = requests.post(url=self.url, files=self.files_payload)
            if self.response.status_code == 201:
                return self.response.json()
        except Exception as e:
            print(e)


    def get_uploaded_files(self):
        self.url: str = self.baseurl + "get-uploaded-files"
        return self.__get_requester(self.url)
    

    def delete_all_files(self):
        self.url: str = self.baseurl + f"delete-all-files"
        try:
            # send Request to server
            self.response: requests = requests.delete(url=self.url)
            # if response is successful
            if self.response.status_code == 204:
                return self.response.json()
        except Exception as e:
            print(e)


    def get_product_description_and_image(self, languages: list[str]):
        # add endpoint
        self.url: str = self.baseurl + "process-data"
        data = {'languages': languages}

        try:
            # send Request to server
            self.response: requests = requests.post(url=self.url, 
                                                    json=data)
            # if response is successful
            if self.response.status_code == 200:
                return self.response.json()
        except Exception as e:
            return None


    def get_saved_settings(self):
        self.url: str = self.baseurl + "get-saved-settings"
        response: any | None = self.__get_requester(self.url)
        if response:
            return response
        else:
            return []


    def set_values_of_settings(self, 
                               user_selected_chunk_size: int, 
                               user_selected_embedding_model: str,
                               user_selected_vector_store: str, 
                               is_image_required: bool,
                               user_selected_llm: str):
        # add endpoint
        self.url: str = self.baseurl + "save-settings"
        data = {'chunk_size': user_selected_chunk_size,
                'embedding_model': user_selected_embedding_model,
                'vector_store': user_selected_vector_store,
                'is_image_required': is_image_required,
                'selected_llm': user_selected_llm}
        try:
            # send Request to server
            self.response: requests = requests.post(url=self.url, 
                                                    json=data)
            # if response is successful
            if self.response.status_code == 200:
                return self.response.json()
        except Exception as e:
            return None