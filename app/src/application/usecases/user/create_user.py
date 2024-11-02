from dataclasses import dataclass
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UsecaseInterface
from app.src.domain.factorys.user_factory import UserDto

@dataclass
class InputDto:
    name: str
    email: str
    password: str
    cpf: str
    birthday: str

@dataclass
class OutputDto:
    user_id: int
    status: str

class CreateUserUsecase(UsecaseInterface):
    def __init__(self, databaseRepository: UserRepositoryInterface):
        self._db_repository = databaseRepository

    def _map_input_dto_to_user_dto(self, input_dto: InputDto)->UserDto:
        return UserDto(name = input_dto.name, email = input_dto.email, password = input_dto.password, cpf = input_dto.cpf, birthday = input_dto.birthday)

    def execute(self, input_dto: InputDto)->OutputDto:
        try:
            user_dto = self._map_input_dto_to_user_dto(input_dto)

            user = self._db_repository.create(user = user_dto)

            return OutputDto(user_id = user.id, status = "User created successfully")
        except Exception as e:
            return OutputDto(user_id = 0, status = str(e))