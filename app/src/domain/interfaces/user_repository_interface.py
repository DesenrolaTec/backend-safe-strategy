from abc import ABC, abstractmethod
from app.src.infra.models.user_model import UserModel

class UserRepositoryInterface(ABC):
    @abstractmethod
    def create(self, is_minimal_user: bool = False) -> None:
        """Método para inserir dados no banco de dados"""
        raise NotImplementedError("O método 'create' precisa ser implementado.")

    @abstractmethod
    def get_by_cpf(self) -> UserModel:
        """Método para ler dados do banco de dados"""
        raise NotImplementedError("O método 'get_by_id' precisa ser implementado.")
    
    @abstractmethod
    def get_by_email(self) -> dict:
        """Método para ler dados do banco de dados"""
        raise NotImplementedError("O método 'get_by_email' precisa ser implementado.")

    @abstractmethod
    def update(self) -> None:
        """Método para atualizar dados no banco de dados"""
        raise NotImplementedError("O método 'update' precisa ser implementado.")

    @abstractmethod
    def delete(self) -> dict:
        """Método para deletar dados do banco de dados"""
        raise NotImplementedError("O método 'delete' precisa ser implementado.")

    # @abstractmethod
    # def close(self) -> None:
    #     """Método para fechar a conexão com o banco de dados"""
    #     raise NotImplementedError("O método 'close' precisa ser implementado.")