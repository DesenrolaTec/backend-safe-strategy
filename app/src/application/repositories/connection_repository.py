from sqlalchemy.orm import Session
from app.src.infra.models.profiles_model import Profile
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface

class ConnectionRepository(ConnectionRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create(self, user_id: int, organization_id: int, role: str, enable: int, client_code: str):
        try:
            profile = Profile(user_id=user_id,
                              organization_id=organization_id,
                              role=role, enable=enable,
                              client_code=client_code)
            self.__session.add(profile)
            self.__session.commit()
            return profile
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError (f"Erro ao criar connection: {e}")

    def get_connection_by_user_id(self, user_id: int):
        profile = self.__session.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            return None
        profile = Profile(user_id=profile.user_id, organization_id=profile.organization_id, role=profile.role, enable=True)
        return profile

    def update(self,):
        pass

    def delete(self,):
        pass