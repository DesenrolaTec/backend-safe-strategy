from app.src.application.usecases.groups.delete_group_usecase import DeleteGroupUsecase
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.groups_controller_interface import GroupsControllerInterface
from app.src.application.usecases.groups.get_groups_usecase import OutputDto

class GroupsController(GroupsControllerInterface):
    def __init__(self,
                 get_groups_usecase: UseCaseInterface,
                 create_group_usecase: UseCaseInterface,
                 delete_group_usecase: DeleteGroupUsecase)->None:
        self.get_groups_usecase = get_groups_usecase
        self.create_group_usecase = create_group_usecase
        self.delete_group_usecase = delete_group_usecase

    def get_groups(self, user_cpf: str):
        output_dto: OutputDto = self.get_groups_usecase.execute(user_cpf = user_cpf)
        return output_dto

    def create_group(self, user_cpf: str, data: dict):
        response: dict = self.create_group_usecase.execute(user_cpf = user_cpf,
                                                                  data = data)
        return response

    def delete_group(self, group_id: int):
        try:
            self.delete_group_usecase.execute(group_id=group_id)
            return None
        except Exception as e:
            raise e