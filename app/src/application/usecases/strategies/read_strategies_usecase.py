from app.src.domain.interfaces.strategies_repository_interface import StrategiesRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface


class ReadStrategiesUsecase(UseCaseInterface):
    def __init__(self,
                 strategies_repository: StrategiesRepositoryInterface):
        self._repository = strategies_repository

    def execute(self):
        try:
            response = []
            strategies = self._repository.get_all_strategies()
            for strategy in strategies:
                response.append(
                    {
                        "id": strategy.id,
                        "name": strategy.name
                    }
                )
            return response
        except Exception as e:
            raise RuntimeError(e)