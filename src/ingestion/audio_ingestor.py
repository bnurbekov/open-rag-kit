import openai
import os

class AudioIngestor:
    def __init__(self, model="whisper-1"):
        self.model = model

    def process(self, file_path: str) -> str:
        """Transcribe audio file using OpenAI Whisper."""
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcriptions.create(
                model=self.model,
                file=audio_file
            )
        return transcript["text"]