from abc import ABC, abstractmethod

class StrategiesRepositoryInterface(ABC):
    @abstractmethod
    def create(self,
               organization_id: int,
               name: str,
               content: str):
        raise NotImplementedError