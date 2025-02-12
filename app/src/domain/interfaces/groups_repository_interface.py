from abc import ABC, abstractmethod
from app.src.domain.classes.groups.dto import GroupsDto

class IgroupsRepository(ABC):
    @abstractmethod
    def get_groups_by_organization(self, organization_id: int)->list[GroupsDto]:
        raise NotImplementedError

    @abstractmethod
    def create_group(self, group_name: str, organization_id: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_group_by_name(self, group_name: str) -> GroupsDto:
        raise NotImplementedError