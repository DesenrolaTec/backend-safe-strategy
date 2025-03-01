from dataclasses import dataclass
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface
from app.src.domain.factorys.user_factory import user_client, MinimalUserFactory

@dataclass
class UserDto:
    user_name: str
    user_email: str
    user_cpf: str
    client_code: str
    user_enable: int
    user_group_ids: list[int]

@dataclass
class OutputDto:
    conn_id: int
    status: str

def map_input_dto_to_user_dto(data: dict)->UserDto:
    return UserDto(user_name = data.get("user_name"),
                   user_email = data.get("user_email"),
                   user_cpf = data.get("user_cpf"),
                   client_code = data.get("user_client_code"),
                   user_enable = data.get("user_enable"),
                   user_group_ids = data.get("user_groups_ids"))

class UpdateConnectionUsecase(UseCaseInterface):
    def __init__(self,
                 conn_repository: ConnectionRepositoryInterface,
                 user_repository: UserRepositoryInterface,
                 groups_has_users_repository: GroupsHasUsersInterface) -> None:
        self._conn_repository = conn_repository
        self._user_repository = user_repository
        self._groups_has_users_repository = groups_has_users_repository
        self._minimal_user_factory = MinimalUserFactory()

    def execute(self, data: dict)->OutputDto:
        try:
            user_dto = map_input_dto_to_user_dto(data)
            user_id = self._user_repository.update_conn(user_dto)

            db_profile = self._conn_repository.update(user_dto, user_id)

            # Recuperar usuarios do grupo
            new_groups = user_dto.user_group_ids
            old_groups = self._groups_has_users_repository.get_groups_by_user_id(user_id)

            groups_to_add = list(set(new_groups) - set(old_groups))
            groups_to_remove = list(set(old_groups) - set(new_groups))

            for group in groups_to_remove:
                self._groups_has_users_repository.delete_user_by_group(user_id=user_id, group_id=group)

            for group in groups_to_add:
                self._groups_has_users_repository.insert(groups_id=group, users_id=user_id)


            return "Conexão atualizada."
        except Exception as e:
            raise e
