from dataclasses import dataclass
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.classes.user import User

@dataclass
class InputDto:
    cpf: str

@dataclass
class OutputDto:
    user: User
    status: str

class DeleteUserUsecase(UseCaseInterface):
    def __init__(self, databaseRepository: UserRepositoryInterface):
        self._db_repository = databaseRepository

    def execute(self, input_dto: InputDto)->OutputDto:
        try:
            user = self._db_repository.delete(input_dto.cpf)
            return OutputDto(user=user, status = "Sucess")
        except Exception as e:
            return OutputDto(user_id = 0, status = str(e))