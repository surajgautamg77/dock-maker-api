from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os

load_dotenv()
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not AZURE_STORAGE_CONNECTION_STRING:
    raise RuntimeError("Set AZURE_STORAGE_CONNECTION_STRING in your .env")

# Replace with your Azure Blob Storage connection string and container name
CONTAINER_NAME = "ai-rep-platform"
 
class AzureBlobManager:
    def __init__(self, connection_string, container_name):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
 
        # Create the container if it doesn't exist
        if not self.container_client.exists():
            self.container_client.create_container()
            print(f"Container '{container_name}' created.")
        else:
            print(f"Container '{container_name}' already exists.")
 
    # Create or Upload a file
    def upload_file(self, blob_name, file):
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            # with open(file_path, "rb") as file:
            pdf_url = blob_client.upload_blob(file, overwrite=True)
            return blob_client.url
            # print(f"File '{file_path}' uploaded to blob '{blob_name}'.")
        except Exception as e:
            print(f"Error uploading file: {e}")
 
    # Read or Download a file
    def download_file(self, blob_name, download_path):
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(download_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
            print(f"Blob '{blob_name}' downloaded to '{download_path}'.")
        except Exception as e:
            print(f"Error downloading file: {e}")
 
    # Update a file (re-upload with the same blob name)
    def update_file(self, blob_name, new_file_path):
        self.upload_file(blob_name, new_file_path)
 
    # Delete a file
    def delete_file(self, blob_name):
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.delete_blob()
            print(f"Blob '{blob_name}' deleted.")
        except Exception as e:
            print(f"Error deleting blob: {e}")
 
    # List all files in the container
    def list_files(self):
        try:
            blobs = self.container_client.list_blobs()
            print("Files in the container:")
            for blob in blobs:
                print(f"- {blob.name}")
        except Exception as e:
            print(f"Error listing blobs: {e}")


azure_blob_manager = AzureBlobManager(AZURE_STORAGE_CONNECTION_STRING, CONTAINER_NAME) 







