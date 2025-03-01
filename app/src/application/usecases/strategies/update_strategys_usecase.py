from app.src.domain.interfaces.strategies_repository_interface import StrategiesRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface


class UpdateStrategysUseCase(UseCaseInterface):
    def __init__(self,
                 strategies_repository: StrategiesRepositoryInterface):
        self.strategies_repository = strategies_repository

    def execute(self,id: int, data: dict):
        try:
            name = data.get("name")
            content = data.get("content")

            self.strategies_repository.update(id = id, name = name, content = content)

            return None
        except Exception as e:
            raise e

