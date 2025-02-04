from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.groups_controller_interface import GroupsControllerInterface
from app.src.application.usecases.groups.get_groups_usecase import OutputDto

class GroupsController(GroupsControllerInterface):
    def __init__(self, get_groups_usecase: UseCaseInterface)->None:
        self.get_groups_usecase = get_groups_usecase

    def get_groups(self, user_cpf: str):
        output_dto: OutputDto = self.get_groups_usecase.execute(user_cpf = user_cpf)
        return output_dto

