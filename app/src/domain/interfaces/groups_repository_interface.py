from abc import ABC, abstractmethod
from app.src.domain.classes.groups.dto import GroupsDto

class IgroupsRepository(ABC):
    @abstractmethod
    def get_groups_by_organization(self, organization_id: int)->list[GroupsDto]:
        raise NotImplementedError