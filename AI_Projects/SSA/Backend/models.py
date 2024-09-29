import openai
from openai import OpenAI
import indicators as ind
from env import Env
import os


class AImodels:
    def __init__(self):
        self.client = OpenAI(api_key=Env.get("OPENAI_API_KEY"))


    def STT(self, audio_file_path):
        try:
            print("reached...")
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file_path,
                response_format='text',
                language='en'
                )
            return transcript
        except Exception as e:
            return f"{ind.error}{e}"
        

    def TTS(self, text: str, voice: str = "alloy"):
        try:
            speech_file_path = os.getcwd() + "/speech.mp3"
            response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
            )
            response.write_to_file(speech_file_path)
            return speech_file_path
        except Exception as e:
            return f"{ind.error}{e}"


