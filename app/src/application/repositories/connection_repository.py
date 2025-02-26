from sqlalchemy.orm import Session

from app.src.infra.models.groups_has_users_model import GroupsHasUsersModel
from app.src.infra.models.groups_model import GroupsModel
from app.src.infra.models.profiles_model import Profile
from app.src.infra.models.user_model import UserModel
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

    def get_all_connections(self):
        try:
            results = self.__session.query.query(
                UserModel.id.label('user_id'),
                UserModel.name.label('user_name'),
                Profile.enable.label('profile_status'),
                GroupsModel.id.label('group_id'),
                GroupsModel.name.label('group_name')
            ).join(Profile, UserModel.id == Profile.user_id) \
                .join(GroupsHasUsersModel, UserModel.id == GroupsHasUsersModel.users_id) \
                .join(GroupsModel, GroupsHasUsersModel.groups_id == GroupsModel.id) \
                .all()
            if not results:
                return None
            return results
        except Exception as e:
            return e


    def update(self,):
        pass

    def delete(self,):
        pass