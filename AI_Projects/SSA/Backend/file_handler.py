import os
import indicators as ind


class FileHandler:
    def __init__(self) -> None:
        self.file_name = "temp_audio"


    def create_temp_file(self, audio_file, extension: str = "wav"):
        try:
            with open(f"{self.file_name}.{extension}", "wb") as f:
                f.write(audio_file.file.read())
            return f"{self.file_name}.{extension}"
        except Exception as e:
            return f"{ind.error}{e}" 
        

    def remove_temp_file(self, file_name):
        try:
            os.remove(file_name)
        except Exception as e:
            return f"{ind.error}{e}"
