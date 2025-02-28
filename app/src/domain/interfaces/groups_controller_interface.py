from abc import ABC, abstractmethod

class GroupsControllerInterface(ABC):
    @abstractmethod
    def get_groups(self, user_cpf: str):
        raise NotImplementedError

    @abstractmethod
    def create_group(self, user_cpf: str, data: dict):
        raise NotImplementedError
    
    @abstractmethod
    def delete_group(self, group_id: int):
        raise NotImplementedError

    @abstractmethod
    def update_group(self, data: dict):
        raise NotImplementedError