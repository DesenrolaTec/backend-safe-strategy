from typing import Optional
from dataclasses import dataclass
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface
from app.src.domain.classes.user import User
from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.interfaces.organization_repository_interface import OrganizationRepositoryInterface


@dataclass
class InputDto:
    cpf: Optional[str]
    email: Optional[str]

@dataclass
class OutputDto:
    user: User
    organization: str
    role: str
    status: str

class ReadUserUsecase(UseCaseInterface):
    def __init__(self,
                 databaseRepository: UserRepositoryInterface,
                 conn_repository: ConnectionRepositoryInterface,
                 organization_repository: OrganizationRepositoryInterface):
        self._db_repository = databaseRepository
        self.__conn_repository = conn_repository
        self.__org_repository = organization_repository

    def execute(self, input_dto: InputDto)->OutputDto:
        try:
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
            profile = self.__conn_repository.get_connection_by_user_id(user_id=user.id)
            organization = self.__org_repository.get_organization_by_organization_id(org_id=profile.organization_id)
            return OutputDto(user = user, organization=organization.name, role=profile.role, status = "Success")
        except Exception as e:
            return OutputDto(user_id = 0, status = str(e))