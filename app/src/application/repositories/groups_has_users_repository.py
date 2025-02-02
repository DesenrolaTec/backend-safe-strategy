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


