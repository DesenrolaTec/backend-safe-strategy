from dataclasses import dataclass
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UsecaseInterface
from app.src.domain.classes.user import User

@dataclass
class InputDto:
    cpf: str

@dataclass
class OutputDto:
    user: User
    status: str

class ReadUserUsecase(UsecaseInterface):
    def __init__(self, databaseRepository: UserRepositoryInterface):
        self._db_repository = databaseRepository

    def execute(self, input_dto: InputDto)->OutputDto:
        try:
            user = self._db_repository.get_by_cpf(input_dto.cpf)
            return OutputDto(user = user, status = "Success")
        except Exception as e:
            return OutputDto(user_id = 0, status = str(e))