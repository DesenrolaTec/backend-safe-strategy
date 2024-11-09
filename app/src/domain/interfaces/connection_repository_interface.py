from abc import ABC, abstractmethod

class ConnectionRepositoryInterface(ABC):
    @abstractmethod
    def create(self) -> None:
        """Método para inserir dados no banco de dados"""
        raise NotImplementedError("O método 'create' precisa ser implementado.")