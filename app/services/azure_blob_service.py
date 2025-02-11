# app/services/azure_blob_service.py

from azure.storage.blob import BlobServiceClient
from typing import Optional

class AzureBlobService:
    def __init__(self, connection_string: str):
        # If no connection string is passed, fetch it from environment variables
        self.connection_string = connection_string or os.getenv('AZURE_CONNECTION_STRING')
        if not self.connection_string:
            raise ValueError("Connection string is required for Azure Blob Service.")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def upload_blob(self, container_name: str, blob_name: str, data: bytes):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data)
        print(f"Blob '{blob_name}' uploaded to container '{container_name}'.")

    def download_blob(self, container_name: str, blob_name: str) -> bytes:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        download_stream = blob_client.download_blob()
        return download_stream.readall()

    async def fetch_blob_image(self, blob_name: str) -> bytes:
        container_name = 'your-container-name'  # Provide the actual container name here
        return self.download_blob(container_name, blob_name)

    # Additional methods can be added as needed, such as listing blobs, deleting blobs, etc.
