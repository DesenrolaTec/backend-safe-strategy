from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.infra.models.profiles_model import Profile
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from dataclasses import dataclass

@dataclass
def Connection() -> None:
    status: int
    user_id: int
    user_name: str
    groups: list

class ReadConnectionsUsecase(UseCaseInterface):
    def __init__(self,
                 conn_repository: ConnectionRepositoryInterface):
        self.conn_repository = conn_repository

    def execute(self):
        try:
            results: list[Profile] = self.conn_repository.get_all_connections()
            response = [
                Connection(
                    status = result.user_name,
                    user_id = result.user_id,
                    user_name = result.user_name,
                    groups = result.group_name
                )
                for result in results
            ]
            return response
        except Exception as e:
            return e
