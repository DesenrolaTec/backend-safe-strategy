from abc import ABC, abstractmethod

class StrategiesControllerInterface(ABC):
    @abstractmethod
    def create_strategies(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete_strategies(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def update_strategies(self, id: int, data: dict):
        raise NotImplementedError