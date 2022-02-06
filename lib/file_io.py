from io import BytesIO

from matplotlib.pyplot import bar

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
            return GCloudFileIO()
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
    pass



default_file_io_factory = EnvironmentFileIOFactory()