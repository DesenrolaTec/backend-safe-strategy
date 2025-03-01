from sqlalchemy.orm import Session
from app.src.infra.models.groups_has_users_model import GroupsHasUsersModel
from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface

class GroupsHasUsersRepository(GroupsHasUsersInterface):
    def __init__(self, session: Session):
        self.__session = session

    def insert(self,
               groups_id: int,
               users_id: int):

        try:
            groups_has_users_model = GroupsHasUsersModel(groups_id=groups_id,
                                                         users_id=users_id)
            self.__session.add(groups_has_users_model)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError(f"Erro ao inserir groups has users: {e}")
        
    def get_groups_by_id(self, group_id: int)->list[GroupsHasUsersModel]:
        try:
            users_id = []
            groups = self.__session.query(GroupsHasUsersModel).filter_by(groups_id=group_id)
            for group in groups:
                users_id.append(group.users_id)
            return users_id
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError(f"Erro ao recuperar groups has users pelo group_id: {e}")

    def get_groups_by_user_id(self, user_id: int)->list[GroupsHasUsersModel]:
        try:
            groups_ids = []
            groups = self.__session.query(GroupsHasUsersModel).filter_by(users_id=user_id)
            for group in groups:
                groups_ids.append(group.groups_id)
            return groups_ids
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError(f"Erro ao recuperar groups has users pelo group_id: {e}")

    def delete_user(self, user_id: int):
        try:
            users = self.__session.query(GroupsHasUsersModel).filter_by(users_id=user_id).first()

            if users:
                self.__session.delete(users)
                self.__session.commit()

        except Exception as e:
            self.__session.rollback()
            raise RuntimeError("Erro ao deletar usuarios")

    def delete_user_by_group(self, user_id: int, group_id: int):
        try:
            users = self.__session.query(GroupsHasUsersModel).filter(
                GroupsHasUsersModel.users_id == user_id,
                GroupsHasUsersModel.groups_id == group_id).first()

            if users:
                self.__session.delete(users)
                self.__session.commit()

        except Exception as e:
            self.__session.rollback()
            raise RuntimeError("Erro ao deletar usuarios")