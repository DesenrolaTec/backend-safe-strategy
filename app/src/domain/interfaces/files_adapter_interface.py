from abc import ABC, abstractmethod


class FilesAdapterInterface(ABC):
    
    @abstractmethod
    def get_full_name(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_base_name(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_extension(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def save(self, path: str) -> None:
        raise NotImplementedError