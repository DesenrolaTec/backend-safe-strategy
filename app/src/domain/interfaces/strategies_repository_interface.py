from abc import ABC, abstractmethod

class StrategiesRepositoryInterface(ABC):
    @abstractmethod
    def create(self,
               organization_id: int,
               name: str,
               content: str):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def update(self,id:int, name: str, content: str):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> list:
        raise NotImplementedError