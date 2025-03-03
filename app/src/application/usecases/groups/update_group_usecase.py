from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository


class UpdateGroupUseCase:
    def __init__(self,
                 groups_has_users_repository: GroupsHasUsersInterface,
                 groups_repository: IgroupsRepository):
        self.gp_has_users_repository = groups_has_users_repository
        self.groups_repository = groups_repository

    def execute(self,
                data: dict):
        try:
            group_id = data.get("group_id")
            group_name = data.get("group_name")
            new_users = data.get("group_users_id")

            #Atualizar nome do grupo
            self.groups_repository.update_group_name(group_id=group_id,
                                                     group_name=group_name)

            #Recuperar usuarios do grupo
            groups = self.gp_has_users_repository.get_groups_by_id(group_id=group_id)
            old_users = []
            for user_id in groups:
                old_users.append(
                    user_id
                )

            users_to_add = list(set(new_users) - set(old_users))
            users_to_remove = list(set(old_users) - set(new_users))

            for user_id in users_to_remove:
                self.gp_has_users_repository.delete_user_by_group(user_id = user_id, group_id = group_id)

            for user_id in users_to_add:
                self.gp_has_users_repository.insert(groups_id=group_id, users_id=user_id)

            return None
        except Exception as e:
            raise e
