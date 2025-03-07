import os
from app.src.domain.interfaces.files_adapter_interface import FilesAdapterInterface
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

class FilesAdapter(FilesAdapterInterface):
    
    def __init__(self, file: FileStorage) -> None:
        self.file = file
        
    def get_full_name(self) -> str:
        return secure_filename(self.file.filename)
    
    def get_base_name(self) -> str:
        base_name, _ = os.path.splitext(secure_filename(self.file.filename))
        return base_name
    
    def get_extension(self) -> str:
        _, file_extension = os.path.splitext(secure_filename(self.file.filename))
        return file_extension
    
    def save(self, path: str) -> None:
        self.file.save(path)        