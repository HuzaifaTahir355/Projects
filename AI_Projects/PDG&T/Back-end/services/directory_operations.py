import os

class DirectoryOperations:
    def get_list_of_files_or_folders(self, path: str = os.getcwd()):
        return os.listdir(path)