from sqlalchemy.orm import Session
from sqlalchemy import func
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
                              role=role,
                              enable=enable,
                              client_code=client_code)
            self.__session.add(profile)
            self.__session.commit()
            return profile
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError (f"Erro ao criar connection: {e}")

    def update(self, user_dto, id):
        try:
            db_profile = self.__session.query(Profile).filter_by(user_id=id).first()
            db_profile.client_code = user_dto.client_code
            db_profile.enable = user_dto.user_enable

            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e


    def get_connection_by_user_id(self, user_id: int):
        profile = self.__session.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            return None
        profile = Profile(user_id=profile.user_id, organization_id=profile.organization_id, role=profile.role, enable=profile.enable, client_code = profile.client_code)
        return profile

    def get_connection_by_id(self, id: int):
        profile = self.__session.query(Profile).filter_by(id=id).first()
        if not profile:
            return None
        profile = Profile(user_id=profile.user_id, organization_id=profile.organization_id, role=profile.role, enable=profile.enable, client_code = profile.client_code)
        return profile

    def get_all_connections(self):
        try:
            results  = self.__session.query(
                        UserModel.id.label('user_id'),
                        UserModel.name.label('user_name'),
                        UserModel.email.label('user_email'),
                        UserModel.cpf.label('user_cpf'),
                        Profile.id.label('profile_id'),
                        Profile.enable.label('profile_status'),
                        Profile.client_code.label('client_code'),
                        func.group_concat(GroupsModel.id).label('group_ids'),
                        func.group_concat(GroupsModel.name).label('group_names')
                    ).join(Profile, UserModel.id == Profile.user_id) \
                    .outerjoin(GroupsHasUsersModel, UserModel.id == GroupsHasUsersModel.users_id) \
                    .outerjoin(GroupsModel, GroupsHasUsersModel.groups_id == GroupsModel.id) \
                    .group_by(UserModel.id, Profile.id, Profile.enable) \
                    .all()
            if not results:
                return None
            return results
        except Exception as e:
            raise e

    def delete(self, conn_id: int, user_id: int):
        try:
            profile_to_delete = self.__session.query(Profile).filter(Profile.id == conn_id).first()

            if profile_to_delete:
                if profile_to_delete.user_id == user_id:
                    raise RuntimeError("Você não pode deletar seu propio usuário.")
                self.__session.delete(profile_to_delete)
                self.__session.commit()
            return None
        except Exception as e:
            raise e