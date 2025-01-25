from typing import Optional
from dataclasses import dataclass
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.classes.user import User

@dataclass
class InputDto:
    cpf: Optional[str]
    email: Optional[str]

@dataclass
class OutputDto:
    user: User
    status: str

class ReadUserUsecase(UseCaseInterface):
    def __init__(self, databaseRepository: UserRepositoryInterface):
        self._db_repository = databaseRepository

    def execute(self, input_dto: InputDto)->OutputDto:
        try:
            if input_dto.email:
                db_user = self._db_repository.get_by_email(input_dto.email)
            if input_dto.cpf:
                db_user = self._db_repository.get_by_cpf(input_dto.cpf)
            if not db_user:
                raise Exception('User not found')
            user = User(
                    id = db_user.id,
                    name = db_user.name,
                    email = db_user.email,
                    cpf = db_user.cpf,
                    password = db_user.password,
                    birthday = db_user.birthday
                )
            return OutputDto(user = user, status = "Success")
        except Exception as e:
            return OutputDto(user_id = 0, status = str(e))