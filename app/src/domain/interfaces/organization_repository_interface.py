from abc import ABC, abstractmethod
from app.src.infra.models.organizations_model import OrganizationModel

class OrganizationRepositoryInterface(ABC):
    @abstractmethod
    def get_organization_by_organization_id(self, org_id: int) -> OrganizationModel:
        raise NotImplementedError