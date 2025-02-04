from typing import Optional
from dataclasses import dataclass
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository

@dataclass
class OutputDto:
    groups: Optional[list]
    status: int
    message: str

class GetGroupsUsecase(UseCaseInterface):
    def __init__(self,
                 repository: IgroupsRepository):
        self.repository = repository

    def execute(self, user_cpf: str):
        try:
            responses = []
            groups = self.repository.get_groups_by_organization(organization_id=1) #TODO: Ajustar usecase para buscar organização do usuario.
            for group in groups:
                responses.append(group.name)
            return OutputDto(status=200,
                             message="Grupos extraidos com sucesso!",
                             groups=responses)
        except Exception as e:
            return OutputDto(status=500,
                             message=f"Erro ao recuperar grupos: {e}")
