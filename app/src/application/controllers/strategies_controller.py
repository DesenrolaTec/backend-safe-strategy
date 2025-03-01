from app.src.application.usecases.strategies.delete_strategy_usecase import DeleteStrategyUseCase
from app.src.application.usecases.strategies.update_strategys_usecase import UpdateStrategysUseCase
from app.src.domain.interfaces.strategies_controller_interface import StrategiesControllerInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.application.usecases.strategies.create_strategies_usecase import InputDto

class StrategiesController(StrategiesControllerInterface):
    def __init__(self,
                 create_strategies_usecase: UseCaseInterface,
                 read_strategies_usecase: UseCaseInterface,
                 delete_strategies_usecase: DeleteStrategyUseCase,
                 update_strategies: UpdateStrategysUseCase)->None:
        self.create_strategies_usecase = create_strategies_usecase
        self.read_strategies_usecase = read_strategies_usecase
        self.delete_strategies_usecase = delete_strategies_usecase
        self.update_strategies = update_strategies

    def create_strategies(self, data: dict):
        try:
            dto = InputDto(name=data.get("name"),
                           content=data.get("content"))
            response: dict = self.create_strategies_usecase.execute(input_dto = dto)
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")

    def read_strategies(self):
        try:
            response: dict = self.read_strategies_usecase.execute()
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")

    def delete_strategies(self, id: int):
        try:
            self.delete_strategies_usecase.execute(id = id)
            return None
        except Exception as e:
            raise e

    def update_strategies(self, id:int, data: dict):
        try:
            self.update_strategies.execute(id = id, data = data)
        except Exception as e:
            raise e