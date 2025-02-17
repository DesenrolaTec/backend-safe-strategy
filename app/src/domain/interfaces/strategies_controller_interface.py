from abc import ABC, abstractmethod

class StrategiesControllerInterface(ABC):
    @abstractmethod
    def create_strategies(self, data: dict):
        raise NotImplementedError