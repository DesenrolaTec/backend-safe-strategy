from dataclasses import dataclass
from gc import enable

from app.src.domain.factorys.user_factory import UserDto
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.factorys.user_factory import user_client, UserDto, MinimalUserFactory

@dataclass
class InputDto:
    user_name: str
    user_email: str
    user_cpf: str
    user_client_id: str
    user_enable: int
    user_groups: list

@dataclass
class OutputDto:
    conn_id: int 
    status: str

def map_input_dto_to_user_dto(input_dto: InputDto)->UserDto:
    return UserDto(name = input_dto.user_name, email = input_dto.user_email, password = "a!vq3jrM-K", cpf = input_dto.user_cpf)

class CreateConnectionUsecase(UseCaseInterface):
    def __init__(self, conn_repository: ConnectionRepositoryInterface, user_repository: UserRepositoryInterface) -> None:
        self._conn_repository = conn_repository
        self._user_repository = user_repository
        self._minimal_user_factory = MinimalUserFactory()

    def execute(self, input_dto: InputDto)->OutputDto:
        try:
            user_dto = map_input_dto_to_user_dto(input_dto)
            db_user = self._user_repository.create(user=user_dto, is_minimal_user=True)
            user_dto = UserDto(id=db_user.id,
                               name=db_user.name,
                               email=db_user.email,
                               cpf=db_user.cpf,
                               password=db_user.password)
            user = user_client(self._minimal_user_factory, user_dto)
            db_profile = self._conn_repository.create(user_id=user.id, role="trader", organization_id=1, enable= input_dto.user_enable)
            return OutputDto(conn_id=db_profile.id, status= "Profile criado com sucesso!")
        except Exception as e:
            return OutputDto(conn_id=000, status=f"Erro ao criar profilçe: {e}")
