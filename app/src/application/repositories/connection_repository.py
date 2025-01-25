from sqlalchemy.orm import Session
from app.src.infra.models.profiles_model import Profile
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface

class ConnectionRepository(ConnectionRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create(self, user_id: int, organization_id: int, role: str):
        profile = Profile(user_id=user_id, organization_id=organization_id, role=role, enable=True)
        self.__session.add(profile)
        self.__session.commit()
        return profile

    def read(self,):
        pass

    def update(self,):
        pass

    def delete(self,):
        pass