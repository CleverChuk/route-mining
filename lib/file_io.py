from io import BytesIO
import os

from matplotlib.pyplot import bar

from google.cloud import storage

MAX_CONTENT_LENGTH = 1000 * 1000 * 1000

class AbstractFileIOFactory:
    def create(self, env: str):
        raise NotImplementedError


class FileIO:
    def read(self, path: str) -> BytesIO:
        raise NotImplementedError

    def write(self, bytes: BytesIO, path: str) -> str:
        raise NotImplementedError


class EnvironmentFileIOFactory(AbstractFileIOFactory):
    def create(self, env: str) -> FileIO:
        if env == "production":
            return GCloudFileIO(os.getenv("GCLOUD_BUCKET"))
        return LocalFileIO()


class LocalFileIO(FileIO):
    def read(self, path: str) -> BytesIO:
        with open(path, "rb") as fp:
            out = BytesIO(fp.read(MAX_CONTENT_LENGTH))

        return out
    
    def write(self, bytes: BytesIO, path: str) -> str:
        with open(path, "wb") as fp:
            fp.write(bytes.getvalue())

        return "files/export.xlsx"


class GCloudFileIO(FileIO):
    def __init__(self, bucket_name) -> None:
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        
    def read(self, path: str) -> BytesIO:
        """Downloads a blob into memory."""
        # Get GCS bucket
        bucket = self.storage_client.bucket(self.bucket_name)

        # Construct a client side representation of a blob.
        blob = bucket.blob(path)
        contents: str = blob.download_as_string()
        return BytesIO(contents)

    def write(self, bytes: BytesIO, path: str) -> str:
        """Uploads a file to the bucket."""
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(path)
        blob.upload_from_file(bytes)

        return blob.public_url




default_file_io_factory = EnvironmentFileIOFactory()