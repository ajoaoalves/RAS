import os
import time
from minio import Minio
from minio.error import S3Error

# Variables
MINIO_URL = "minio:9000"  # MinIO service name in Docker Compose
MINIO_ROOT_USER = "ROOTNAME"
MINIO_ROOT_PASSWORD = "CHANGEME123"
BUCKET_NAME = "images"
SRC_DIR = "./images/src"  # Path to the folder with input images

# Connect to MinIO
client = Minio(
    MINIO_URL,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False  # Set to True if using HTTPS
)

# Function to wait for MinIO availability
def wait_for_minio():
    print("Waiting for MinIO to be accessible...")
    while True:
        try:
            client.list_buckets()  # Checks if MinIO is accessible
            print("MinIO is accessible!")
            break
        except S3Error:
            time.sleep(2)

# Function to create the bucket and folders inside it
import io  # Biblioteca para criar streams em memória

def setup_bucket_structure():
    # Ensure bucket exists
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

    # Create folder structure in the bucket
    folders = ["image/src/", "image/out/"]
    for folder in folders:
        try:
            # Use an in-memory stream for empty content
            empty_stream = io.BytesIO(b"")
            client.put_object(BUCKET_NAME, folder, data=empty_stream, length=0)
            print(f"Folder '{folder}' created in bucket '{BUCKET_NAME}'.")
        except S3Error as e:
            print(f"Error creating folder '{folder}': {e}")


# Function to upload images to the src folder in the bucket
def upload_images():
    print(f"Uploading images from '{SRC_DIR}' to 'image/src/' in bucket '{BUCKET_NAME}'...")
    for file in os.listdir(SRC_DIR):
        file_path = os.path.join(SRC_DIR, file)
        if os.path.isfile(file_path):
            object_name = f"image/src/{file}"  # Path inside the bucket
            try:
                client.fput_object(BUCKET_NAME, object_name, file_path)
                print(f"Image '{file}' successfully uploaded to '{object_name}'.")
            except S3Error as e:
                print(f"Error uploading the image '{file}': {e}")

# Main execution
if __name__ == "__main__":
    wait_for_minio()             # Wait for MinIO to be accessible
    setup_bucket_structure()     # Create bucket and folder structure
    upload_images()              # Upload images to image/src
    print("MinIO setup completed!")
