from abc import ABC, abstractmethod
from app.src.infra.models.profiles_model import Profile

class ConnectionRepositoryInterface(ABC):
    @abstractmethod
    def create(self, user_id: int, organization_id: int, role: str) -> Profile:
        raise NotImplementedError("O método 'create' precisa ser implementado.")

    @abstractmethod
    def get_connection_by_user_id(self, user_id: int) -> Profile:
        raise NotImplementedError

    @abstractmethod
    def update(self,):
        raise NotImplementedError

    @abstractmethod
    def delete(self,):
        raise NotImplementedError

