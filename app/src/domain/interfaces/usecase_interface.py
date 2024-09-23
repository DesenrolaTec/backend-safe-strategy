from abc import ABC, abstractmethod

class UsecaseInterface(ABC):
    @abstractmethod
    def execute(self, inputDto):
        """Método para inserir dados no banco de dados"""
        raise NotImplementedError("O método 'execute' precisa ser implementado.")