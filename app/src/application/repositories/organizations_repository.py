from sqlalchemy.orm import Session
from app.src.infra.models.organizations_model import OrganizationModel
from app.src.domain.interfaces.organization_repository_interface import OrganizationRepositoryInterface

class OrganizationRepository(OrganizationRepositoryInterface):
    def __init__(self, session: Session):
        self.__session = session

    def get_organization_by_organization_id(self, org_id: int) -> OrganizationModel:
        organization = self.__session.query(OrganizationModel).filter_by(id=org_id).first()
        if not organization:
            return None
        return organization