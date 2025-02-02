from abc import ABC, abstractmethod

class GroupsHasUsersInterface(ABC):
    def insert(self,
               groups_id: int,
               users_id: int):
        raise NotImplementedError