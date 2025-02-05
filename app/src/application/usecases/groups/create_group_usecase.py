from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface


class CreateGroupUsecase(UseCaseInterface):
    def __init__(self,
                 groups_has_users_repository: GroupsHasUsersInterface,
                 groups_repository: IgroupsRepository,
                 users_repository: UserRepositoryInterface):
        self.groups_repository = groups_repository
        self.groups_has_users_repository = groups_has_users_repository
        self.users_repository = users_repository

    def execute(self, user_cpf: str, data: dict):
        #TODO: Implementar busca de organização
        try:
            organization_id = 1
            group_name = data.get("group_name")
            group_users_cpf = data.get("group_users_cpf")

            self.groups_repository.create_group(group_name=group_name,
                                                organization_id=organization_id)

            for cpf in group_users_cpf:
                user_id = self.users_repository.get_by_cpf(user_cpf = cpf).id
                self.groups_has_users_repository.insert(group_name=group_name,
                                                        users_id=user_id)
            return {"Sucesso ao criar grupo", 200}
        except Exception as e:
            return {f"{e}", 500}

