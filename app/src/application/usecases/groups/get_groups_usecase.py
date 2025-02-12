from typing import Optional
from dataclasses import dataclass
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface

@dataclass
class OutputDto:
    groups: Optional[list]
    status: int
    message: str

class GetGroupsUsecase(UseCaseInterface):
    def __init__(self,
                 groups_repository: IgroupsRepository,
                 group_has_user_repository: GroupsHasUsersInterface,
                 user_repository: UserRepositoryInterface):
        self.groups_repository = groups_repository
        self.group_has_user = group_has_user_repository
        self.user_repository = user_repository

    def execute(self, user_cpf: str):
        try:
            responses = []
            users = []
            groups = self.groups_repository.get_groups_by_organization(organization_id=1) #TODO: Ajustar usecase para buscar organização do usuario.
            for group in groups:
                group_id = group.id
                users_ids = self.group_has_user.get_groups_by_id(group_id=group_id)
                for id in users_ids:
                    user = self.user_repository.get_by_id(user_id = id)
                    user_name = user.name
                    users.append(
                        {"id": id,
                         "name": user_name}
                    )
                responses.append(
                    {
                        "id": group_id,
                        "name": group.name,
                        "users": users
                    }
                )
                users = []
            return OutputDto(status=200,
                             message="Grupos extraidos com sucesso!",
                             groups=responses)
        except Exception as e:
            return OutputDto(status=500,
                             message=f"Erro ao recuperar grupos: {e}")
