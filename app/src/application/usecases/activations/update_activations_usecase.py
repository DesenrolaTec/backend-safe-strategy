from app.src.domain.interfaces.activations_has_groups_repository import ActivationsHasGroupsRepositoryInterface
from app.src.domain.interfaces.activations_repository_interface import ActivationsRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.application.repositories.activations.activations_repository import ActivationDto


class UpdateActivationsUsecase(UseCaseInterface):
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

    def execute(self, data: dict, activation_id):
        try:
            act_dto = self.map_activation_dto(data=data)
            act_db = self.activations_repository.update(act_dto, activation_id)

            old_groups = self.activations_has_groups.read_activations_by_id(id=activation_id)
            old_acts = []
            for gp in old_groups:
                old_acts.append(
                    gp.groups_id
                )

            groups = data.get("groups", None)

            new_acts = []
            if groups:
                for group in groups:
                    new_acts.append(
                        group.get("group_id")
                    )

            acts_to_add = list(set(new_acts) - set(old_acts))
            acts_to_remove = list(set(old_acts) - set(new_acts))

            for group in acts_to_remove:
                self.activations_has_groups.delete(activation_id=activation_id, group_id=group)

            for group in acts_to_add:
                self.activations_has_groups.insert(activation_id=activation_id, group_id=group)

            return True
        except Exception as e:
            raise e

