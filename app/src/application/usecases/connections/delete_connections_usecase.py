from app.src.application.repositories.groups_has_users_repository import GroupsHasUsersRepository
from app.src.application.repositories.user_repository import UserRepository
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface


class DeleteConnectionsUsecase(UseCaseInterface):
    def __init__(self,
                 conn_repository: ConnectionRepositoryInterface,
                 groups_has_users: GroupsHasUsersRepository,
                 users_repository: UserRepository):
        self.conn_repository = conn_repository
        self.groups_has_users = groups_has_users
        self.users_repository = users_repository

    def execute(self, conn_id: int, user_id: int):
        try:
            user_to_remove = self.conn_repository.get_connection_by_id(conn_id)
            self.conn_repository.delete(conn_id=conn_id, user_id = user_id)
            self.groups_has_users.delete_user(user_id=user_to_remove.user_id)
            self.users_repository.delete_by_id(id=user_to_remove.user_id)
            return None
        except Exception as e:
            raise e