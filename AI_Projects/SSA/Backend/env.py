import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    def get(var_name: str):
        return os.getenv(var_name)
