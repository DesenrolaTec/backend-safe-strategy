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
            group_users_id = data.get("group_users_id")

            self.groups_repository.create_group(group_name=group_name,
                                                organization_id=organization_id)

            group_id = self.groups_repository.get_group_by_name(group_name=group_name).id

            for id in group_users_id:
                self.groups_has_users_repository.insert(groups_id=group_id,
                                                        users_id=id)
            return {"message": "Sucesso ao criar grupo", "status": 200}
        except Exception as e:
            raise RuntimeError(f"{e}")

