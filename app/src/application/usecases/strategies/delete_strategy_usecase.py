from app.src.domain.interfaces.strategies_repository_interface import StrategiesRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface


class DeleteStrategyUseCase(UseCaseInterface):
    def __init__(self,
                 strategies_repository: StrategiesRepositoryInterface):
        self.strategies_repository = strategies_repository

    def execute(self,
                id: int):
        try:
            self.strategies_repository.delete(id=id)
            return None
        except Exception as e:
            raise e
