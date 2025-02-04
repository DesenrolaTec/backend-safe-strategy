from app.src.application.controllers.user_controller import UserController
from app.src.application.controllers.connection_controller import ConnectionController
from app.src.application.controllers.groups_controller import GroupsController

from app.src.application.usecases.user.create_user import CreateUserUsecase
from app.src.application.usecases.user.get_user import ReadUserUsecase
from app.src.application.usecases.user.update_user import UpdateUserUsecase
from app.src.application.usecases.user.delete_user import DeleteUserUsecase
from app.src.application.usecases.connections.create_connection_usecase import CreateConnectionUsecase
from app.src.application.usecases.groups.get_groups_usecase import GetGroupsUsecase

from app.src.application.repositories.user_repository import UserRepository
from app.src.application.repositories.groups.groups_repository import GroupsRepository
from app.src.application.repositories.connection_repository import ConnectionRepository
from app.src.application.repositories.organizations_repository import OrganizationRepository
from app.src.application.repositories.groups_has_users_repository import GroupsHasUsersRepository

from app.src.infra.adapters.sql_alchemy_adapter import db


class Bootstrap:
    def __init__(self):
        self.load_dependencies()

    def load_dependencies(self):
        session = db.session

        org_repo = OrganizationRepository(session=session)
        conn_repository = ConnectionRepository(session=session)
        user_repository = UserRepository(session=session)
        groups_repository = GroupsRepository(session=session)
        groups_has_users = GroupsHasUsersRepository(session=session)

        create_user = CreateUserUsecase(user_repository)
        read_user = ReadUserUsecase(user_repository, conn_repository, organization_repository=org_repo)
        update_user = UpdateUserUsecase(user_repository)
        delete_user = DeleteUserUsecase(user_repository)
        self.user_controller = UserController(create_user=create_user, get_user=read_user, update_user=update_user, delete_user=delete_user)

        conn_usecase = CreateConnectionUsecase(conn_repository, user_repository, groups_has_users)
        self.connection_controller = ConnectionController(conn_usecase)

        get_groups_usecase = GetGroupsUsecase(repository=groups_repository)
        self.groups_controller = GroupsController(get_groups_usecase=get_groups_usecase)