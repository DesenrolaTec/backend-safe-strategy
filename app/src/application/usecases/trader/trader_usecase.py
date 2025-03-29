import os
from app.src.domain.interfaces.activations_has_groups_repository import ActivationsHasGroupsRepositoryInterface
from app.src.domain.interfaces.activations_repository_interface import ActivationsRepositoryInterface
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.interfaces.groups_has_users_repository_interface import GroupsHasUsersInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from dataclasses import dataclass

@dataclass
class ActivationDto:
    activation_id: int
    organization_id: int
    strategy_id: int
    start_at: str
    stop_at: str
    client_code: str
    file_url: str


class TraderUsecase(UseCaseInterface):
    def __init__(self,
                 activations_repository: ActivationsRepositoryInterface,
                 activations_has_groups_repository: ActivationsHasGroupsRepositoryInterface,
                 user_repository: UserRepositoryInterface,
                 gp_has_users: GroupsHasUsersInterface,
                 conn_repository: ConnectionRepositoryInterface):
        self.activations_repository = activations_repository
        self.activations_has_groups_repository = activations_has_groups_repository
        self.user_repository = user_repository
        self.gp_has_users = gp_has_users
        self.conn_repository = conn_repository

    def execute(self, user_cpf):
        try:
            user = self.user_repository.get_by_cpf(user_cpf)
            user_id = user.id
            conn = self.conn_repository.get_connection_by_user_id(user_id=user_id)

            user_groups = self.gp_has_users.get_groups_by_user_id(user_id)

            activations_ids = []
            for group_id in user_groups:
                acts = self.activations_has_groups_repository.read_activations_by_group(groups_id=group_id)
                for act in acts:
                    activations_ids.append(
                        act.activations_id
                    )

            activations_ids = list(set(activations_ids))
            activations = []
            for id in activations_ids:
                act = self.activations_repository.read_id(activation_id=id)
                activations.append(
                    ActivationDto(
                        activation_id=act.id,
                        organization_id = act.organization_id,
                        strategy_id = act.strategy_id,
                        start_at = act.start_at,
                        stop_at = act.stop_at,
                        client_code=conn.client_code,
                        file_url = f"https://app.safestrategy.com.br{act.file_url}"
                    )
                )

            return activations
        except Exception as e:
            raise e
