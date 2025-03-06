from app.src.application.usecases.activations.create_activation_usecase import CreateActivationUseCase
from app.src.application.usecases.activations.read_activations_usecase import ReadActivationsUsecase
from app.src.domain.interfaces.activations_controller_interface import ActivationsControllerInterface


class ActivationsController(ActivationsControllerInterface):
    def __init__(self,
                 read_activation_usecase: ReadActivationsUsecase,
                 create_activation_usecase: CreateActivationUseCase):
        self.read_activation_usecase = read_activation_usecase
        self.create_activation_usecase = create_activation_usecase

    def read_activations(self) -> list:
        try:
            responses = []
            results = self.read_activation_usecase.execute()
            for result in results:
                responses.append(
                    result.__dict__
                )
            return responses
        except Exception as e:
            raise e

    def create_activations(self, data):
        try:
            response = self.create_activation_usecase.execute(data)
            return response
        except Exception as e:
            raise e