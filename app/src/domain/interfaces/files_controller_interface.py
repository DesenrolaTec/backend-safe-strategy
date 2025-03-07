from abc import ABC, abstractmethod

from app.src.domain.interfaces.files_adapter_interface import FilesAdapterInterface

class FilesControllerInterface(ABC):

    @abstractmethod
    def create_file(self, file: FilesAdapterInterface):
        raise NotImplementedError
