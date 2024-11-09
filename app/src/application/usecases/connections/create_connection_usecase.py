from dataclasses import dataclass
from app.src.domain.factorys.user_factory import UserDto
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface

@dataclass
class InputDto:
    email: str
    organization_id: int
    role: str

@dataclass
class OutputDto:
    conn_id: int 
    status: str

class CreateConnectionUsecase(UseCaseInterface):
    def __init__(self, conn_repository: ConnectionRepositoryInterface, user_repository: UserRepositoryInterface) -> None:
        self._conn_repository = conn_repository
        self._user_repository = user_repository

    def execute(self, input_dto: InputDto)->OutputDto:
        user_email = input_dto.email
        organization_id = input_dto.organization_id
        role = input_dto.role

        user = self._user_repository.get_by_email(user_email)

        if not user:
            user_dto = UserDto(email=user_email)
            user = self._user_repository.create(user = user_dto)

        conn = self._conn_repository.create(user_id=user.id, organization_id=organization_id, role=role)
        return OutputDto(conn_id=conn.id, status="Connection created successfully")
