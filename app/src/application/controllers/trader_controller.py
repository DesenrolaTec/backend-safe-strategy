from app.src.application.usecases.trader.trader_usecase import TraderUsecase
from app.src.domain.interfaces.trader_controller_interface import TraderControllerInterface


class TraderController(TraderControllerInterface):
    def __init__(self,
                 trader_usecase: TraderUsecase)->None:
        self.trader_usecase = trader_usecase

    def get_user_activations(self, user_cpf):
        try:
            activations_dto = self.trader_usecase.execute(user_cpf=user_cpf)
            response = []
            for act in activations_dto:
                response.append(
                    act.__dict__
                )
            return response
        except Exception as e:
            raise RuntimeError(f"{e}")