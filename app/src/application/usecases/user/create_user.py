from dataclasses import dataclass
from uuid import uuid4

from app.src.application.repositories.connection_repository import ConnectionRepository
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.factorys.user_factory import UserDto
from app.src.domain.classes.user import User
from app.src.domain.factorys.user_factory import user_client, UserDto, MinimalUserFactory

@dataclass
class InputDto:
    name: str
    email: str
    password: str
    cpf: str
    birthday: str

@dataclass
class OutputDto:
    user: User
    status: str

class CreateUserUsecase(UseCaseInterface):
    def __init__(self,
                 databaseRepository: UserRepositoryInterface,
                 profile_repository: ConnectionRepository):
        self._db_repository = databaseRepository
        self._minimal_user_factory = MinimalUserFactory()
        self.profile_repository = profile_repository

    def _map_input_dto_to_user_dto(self, input_dto: InputDto)->UserDto:
        return UserDto(name = input_dto.name, email = input_dto.email, password = input_dto.password, cpf = input_dto.cpf, birthday = input_dto.birthday)

    def execute(self, input_dto: InputDto)->OutputDto:
        try:
            user_dto = self._map_input_dto_to_user_dto(input_dto)
            db_user = self._db_repository.create(user = user_dto)
            self.profile_repository.create(user_id=db_user.id,organization_id=1,role="owner",client_code=str(uuid4()), enable=1)
            user_dto = UserDto(id=db_user.id,
                               name=db_user.name,
                               email=db_user.email,
                               cpf=db_user.cpf,
                               password=db_user.password,
                               birthday=db_user.birthday)
            user = user_client(self._minimal_user_factory, user_dto)
            return OutputDto(user = user, status = "User created successfully")
        except Exception as e:
            return OutputDto(user_id = None, status = str(e))