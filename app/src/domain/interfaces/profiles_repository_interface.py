from abc import ABC, abstractmethod

class ProfilesRepositoryInterface(ABC):
    @abstractmethod
    def create(self) -> None:
        """Método para inserir dados no banco de dados"""
        raise NotImplementedError("O método 'create' precisa ser implementado.")

    @abstractmethod
    def get_profiles_by_organization(self) -> dict:
        """Método para ler dados do banco de dados"""
        raise NotImplementedError("O método 'get_by_id' precisa ser implementado.")