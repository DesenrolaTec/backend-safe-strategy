from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.infra.models.profiles_model import Profile
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from dataclasses import dataclass

@dataclass
class Connection:
    status: int
    client_code: str
    profile_id: int
    user_id: int
    user_name: str
    user_email: str
    user_cpf: str
    groups: list

class ReadConnectionsUsecase(UseCaseInterface):
    def __init__(self,
                 conn_repository: ConnectionRepositoryInterface):
        self.conn_repository = conn_repository

    def execute(self):
        try:
            results = self.conn_repository.get_all_connections()
            response = []
            for result in results:
                groups = []
                if result.group_ids:
                    group_ids = result.group_ids.split(',')
                    group_names = result.group_names.split(',')
                
                    for index, group in enumerate(group_names):
                        groups.append(
                            {
                                "id": group_ids[index],
                                "name": group
                            }
                        )
                response.append(
                    Connection(
                        status=result.profile_status,
                        client_code=result.client_code,
                        profile_id=result.profile_id,
                        user_id=result.user_id,
                        user_name=result.user_name,
                        user_email=result.user_email,
                        user_cpf=result.user_cpf,
                        groups=groups
                    )
                )
            return response
        except Exception as e:
            raise e
