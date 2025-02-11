# # app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'api-key-value')
        self.OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # Add this line

settings = Settings()


# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     def __init__(self):
#         self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')
#         self.AZURE_CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING', 'default_value_if_missing')
#         self.AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME', 'default_value_if_missing')
        
# settings = Settings()