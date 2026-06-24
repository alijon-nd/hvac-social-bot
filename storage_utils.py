import os
from google.cloud import storage
from config import GCS_BUCKET_NAME, GCS_FOLDER_PATH

def get_storage_client():
    """Initialize Google Cloud Storage client."""
    return storage.Client()

def list_images_in_folder():
    """List all image files in the configured GCS folder."""
    client = get_storage_client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=GCS_FOLDER_PATH)

    images = []
    for blob in blobs:
        name = blob.name
        if name == GCS_FOLDER_PATH:  # skip folder itself
            continue
        if name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            images.append({
                'name': name,
                'blob': blob
            })
    return images

def download_image(blob, destination_path):
    """Download a blob to a local file."""
    blob.download_to_filename(destination_path)
    return destination_path

def delete_image(blob):
    """Delete a blob from the bucket (optional)."""
    blob.delete()