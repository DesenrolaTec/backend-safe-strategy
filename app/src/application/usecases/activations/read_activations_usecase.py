import os
from dataclasses import dataclass

from app.src.application.repositories.activations.activations_repository import ActivationsRepository
from app.src.application.repositories.strategies.strategies_repository import StrategiesRepository
from app.src.domain.interfaces.activations_has_groups_repository import ActivationsHasGroupsRepositoryInterface
from app.src.domain.interfaces.activations_repository_interface import ActivationsRepositoryInterface
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository
from app.src.domain.interfaces.usecase_interface import UseCaseInterface


@dataclass
class GroupDto:
    group_id: int
    group_name: str

@dataclass
class ActivationDto:
    activation_id: int
    strategy_id: int
    strategy_name: str
    strategy_content: str
    groups: list[GroupDto]
    file_url: str
    start_at: str
    stop_at: str

class ReadActivationsUsecase(UseCaseInterface):
    def __init__(self,
                 groups_repository: IgroupsRepository,
                 activations_repository: ActivationsRepositoryInterface,
                 activation_has_groups_repository: ActivationsHasGroupsRepositoryInterface,
                 strategy_repository: StrategiesRepository):
        self.groups_repository = groups_repository
        self.activations_repository = activations_repository
        self.activation_has_groups_repository = activation_has_groups_repository
        self.strategy_repository = strategy_repository

    def execute(self):
        try:
            activations = self.activations_repository.read_all()

            if not activations:
                return None

            responses = []
            for act in activations:
                activation_id = act.id
                strategy_id = act.strategy_id
                start_at = act.start_at.strftime('%Y-%m-%d %H:%M:%S')
                stop_at = act.stop_at.strftime('%Y-%m-%d %H:%M:%S')
                file_url = f"{os.getenv('DOWLOAD_ENDPOINT_URL')}{act.file_url}"

                groups_dto = []
                groups = self.activation_has_groups_repository.read_activations_by_id(id=activation_id)

                if groups:
                    for group in groups:
                        group_id = group.groups_id
                        group_model = self.groups_repository.get_group_by_id(group_id=group_id)
                        groups_dto.append(
                            GroupDto(
                                group_id=group_id,
                                group_name=group_model.name
                            ).__dict__
                        )

                strategy = self.strategy_repository.get_by_id(id=strategy_id)

                responses.append(
                    ActivationDto(
                        activation_id=activation_id,
                        strategy_id=strategy_id,
                        strategy_name=strategy.name,
                        strategy_content=strategy.content,
                        groups=groups_dto,
                        start_at=start_at,
                        stop_at=stop_at,
                        file_url=file_url
                    )
                )

            return responses
        except Exception as e:
            raise e