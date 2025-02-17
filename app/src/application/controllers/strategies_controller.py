from app.src.domain.interfaces.strategies_controller_interface import StrategiesControllerInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.application.usecases.strategies.strategies_usecase import InputDto

class StrategiesController(StrategiesControllerInterface):
    def __init__(self,
                 create_strategies_usecase: UseCaseInterface)->None:
        self.create_strategies_usecase = create_strategies_usecase

    def create_strategies(self, data: dict):
        try:
            dto = InputDto(name=data.get("name"),
                           content=data.get("content"))
            response: dict = self.create_strategies_usecase.execute(input_dto = dto)
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")