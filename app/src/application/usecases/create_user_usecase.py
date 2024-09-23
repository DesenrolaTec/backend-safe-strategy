from typing import Final
from dataclasses import dataclass
from app.src.domain.classes.user import User
from app.src.domain.interfaces.database_interface import DatabaseInterface
from app.src.domain.interfaces.usecase_interface import UsecaseInterface

@dataclass()
class InputDto:
    name: str
    email: str
    password: str
    cpf: Final[str]
    birthday: Final[str]

class CreateUserUsecase(UsecaseInterface):
    def __init__(self, databaseRepository: DatabaseInterface):
        self.__db_repository = databaseRepository

    def execute(self, input_dto: InputDto)->InputDto:
        user = User(name=input_dto.name,
                    email=input_dto.email,
                    password=input_dto.password,
                    cpf=input_dto.cpf,
                    birthday=input_dto.birthday)
        self.__db_repository.create(user = user)
        return input_dto

