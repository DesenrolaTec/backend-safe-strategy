from typing import Optional
from abc import ABC, abstractmethod

class UserControllerInterface(ABC):

    @abstractmethod
    def create_user(self, user_data: dict):
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_cpf: Optional[str], user_email: Optional[str]):
        raise NotImplementedError
    
    @abstractmethod
    def delete_user(self, user_cpf: str):
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user_data: dict):
        raise NotImplementedError
    
    @abstractmethod
    def update_password(self, user_data: dict):
        raise NotImplementedError