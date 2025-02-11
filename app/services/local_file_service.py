# app/services/local_file_service.py

import os

class LocalFileService:
    def __init__(self, file_directory: str = "uploads/"):
        self.file_directory = file_directory

        # Ensure the directory exists
        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

    def save_file(self, file_content: bytes, filename: str):
        file_path = os.path.join(self.file_directory, filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        print(f"File '{filename}' saved locally at '{self.file_directory}'.")

    def fetch_file(self, filename: str) -> bytes:
        file_path = os.path.join(self.file_directory, filename)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File '{filename}' not found locally.")
