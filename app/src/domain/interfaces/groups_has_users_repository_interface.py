from abc import ABC, abstractmethod
from app.src.infra.models.groups_has_users_model import GroupsHasUsersModel

class GroupsHasUsersInterface(ABC):
    @abstractmethod
    def insert(self,
               groups_id: int,
               users_id: int):
        raise NotImplementedError
    
    @abstractmethod
    def get_groups_by_id(self, group_id: int)->list[GroupsHasUsersModel]:
        raise NotImplementedError