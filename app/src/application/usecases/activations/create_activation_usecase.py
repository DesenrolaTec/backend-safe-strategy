from app.src.domain.interfaces.activations_has_groups_repository import ActivationsHasGroupsRepositoryInterface
from app.src.domain.interfaces.activations_repository_interface import ActivationsRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.application.repositories.activations.activations_repository import ActivationDto


class CreateActivationUseCase(UseCaseInterface):
    def __init__(self,
                 activations_repository: ActivationsRepositoryInterface,
                 activations_has_groups: ActivationsHasGroupsRepositoryInterface):
        self.activations_repository = activations_repository
        self.activations_has_groups = activations_has_groups

    @staticmethod
    def map_activation_dto(data: dict) -> ActivationDto:
        return ActivationDto(
            organization_id=data.get("organization_id"),
            strategy_id=data.get("strategy_id"),
            start_at=data.get("start_at"),
            stop_at=data.get("stop_at"),
            file_url=data.get("file_url")
        )

    def execute(self, data: dict):
        try:
            act_dto = self.map_activation_dto(data=data)
            act_db = self.activations_repository.create(data=act_dto)

            for group in data.get("groups"):
                group_id = group.get("group_id")
                self.activations_has_groups.insert(activation_id=act_db.id, group_id=group_id)

            return True
        except Exception as e:
            raise e