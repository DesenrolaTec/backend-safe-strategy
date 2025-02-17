from dataclasses import dataclass
from app.src.domain.interfaces.strategies_repository_interface import StrategiesRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface

@dataclass
class InputDto:
    name: str
    content: str

class CreateStrategiesUsecase(UseCaseInterface):
    def __init__(self, strategies_repository: StrategiesRepositoryInterface):
        self._repository = strategies_repository

    def execute(self, input_dto: InputDto):
        try:
            self._repository.create(organization_id=1,
                                    name=input_dto.name,
                                    content=input_dto.content)

            return "Estrategia criada com sucesso"
        except Exception as e:
            raise RuntimeError(f"Erro ao criar a estrategia: {e}")
