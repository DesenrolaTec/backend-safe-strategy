from abc import ABC, abstractmethod

class ConnectionControllerInterface(ABC):

    @abstractmethod
    def create_connection(self, conn_data: dict):
        raise NotImplementedError