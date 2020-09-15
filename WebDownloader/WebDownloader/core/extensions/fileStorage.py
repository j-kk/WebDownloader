from google.cloud import storage
from pathlib import Path

from WebDownloader.core.config import config


if hasattr(config, 'BUCKET_NAME'):

    def upload_blob(filepath: Path):
        """Uploads a file to the bucket."""

        storage_client = storage.Client()
        bucket = storage_client.bucket(config.BUCKET_NAME)
        blob = bucket.blob(filepath.name)

        blob.upload_from_filename(filepath)

        filepath.unlink()

    def make_blob_public(blob_name):
        """Makes a blob publicly accessible."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(config.BUCKET_NAME)
        blob = bucket.blob(blob_name)

        blob.make_public()

        return blob.public_url


else:
    def upload_blob(*args):
        pass

    def make_blob_public(blob_name):
        print("NO ACCESS TO BUCKET")
        exit(1)
        pass

