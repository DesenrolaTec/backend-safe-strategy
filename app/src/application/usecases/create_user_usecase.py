from typing import Optional
from typing import Final
from dataclasses import dataclass
from app.src.domain.classes.user import User
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UsecaseInterface

@dataclass()
class InputDto:
    name: Optional[str]
    email: str
    password: Optional[str]
    cpf: Optional[str]
    birthday: Optional[str]

class CreateUserUsecase(UsecaseInterface):
    def __init__(self, databaseRepository: UserRepositoryInterface):
        self.__db_repository = databaseRepository

    def execute(self, input_dto: InputDto)->InputDto:
        user = User(name=input_dto.name,
                    email=input_dto.email,
                    password=input_dto.password,
                    cpf=input_dto.cpf,
                    birthday=input_dto.birthday)
        self.__db_repository.create(user = user)
        return input_dto

