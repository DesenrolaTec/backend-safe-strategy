from app.src.domain.interfaces.activations_has_groups_repository import ActivationsHasGroupsRepositoryInterface
from app.src.domain.interfaces.activations_repository_interface import ActivationsRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface


class DeleteActivationsUsecase(UseCaseInterface):
    def __init__(self,
                 activations_repository: ActivationsRepositoryInterface,
                 activations_has_groups: ActivationsHasGroupsRepositoryInterface):
        self.activations_repository = activations_repository
        self.activations_has_groups = activations_has_groups

    def execute(self, activation_id: int):
        try:
            self.activations_repository.delete(activation_id=activation_id)
            self.activations_has_groups.delete_by_id(activation_id=activation_id)
            return True
        except Exception as e:
            raise e

