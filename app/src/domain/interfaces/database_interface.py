from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def create(self) -> None:
        """Método para inserir dados no banco de dados"""
        raise NotImplementedError("O método 'create' precisa ser implementado.")

    @abstractmethod
    def read(self) -> dict:
        """Método para ler dados do banco de dados"""
        raise NotImplementedError("O método 'read' precisa ser implementado.")

    # @abstractmethod
    # def update(self) -> None:
    #     """Método para atualizar dados no banco de dados"""
    #     raise NotImplementedError("O método 'update' precisa ser implementado.")

    # @abstractmethod
    # def delete(self) -> None:
    #     """Método para deletar dados do banco de dados"""
    #     raise NotImplementedError("O método 'delete' precisa ser implementado.")

    # @abstractmethod
    # def close(self) -> None:
    #     """Método para fechar a conexão com o banco de dados"""
    #     raise NotImplementedError("O método 'close' precisa ser implementado.")
