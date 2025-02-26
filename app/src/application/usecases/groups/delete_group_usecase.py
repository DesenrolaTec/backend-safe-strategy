from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository


class DeleteGroupUsecase:
    def __init__(self,
                 groups_repository: IgroupsRepository):
        self.groups_repository = groups_repository

    def execute(self, group_id):
        try:
            self.groups_repository.delete_group(group_id=group_id)
            return None
        except Exception as e:
            raise e