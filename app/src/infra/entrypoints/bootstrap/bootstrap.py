from app.src.application.controllers.strategies_controller import StrategiesController
from app.src.application.controllers.user_controller import UserController
from app.src.application.controllers.connection_controller import ConnectionController
from app.src.application.controllers.groups_controller import GroupsController
from app.src.application.repositories.strategies.strategies_repository import StrategiesRepository
from app.src.application.usecases.connections.delete_connections_usecase import DeleteConnectionsUsecase
from app.src.application.usecases.connections.read_connections_usecase import ReadConnectionsUsecase
from app.src.application.usecases.groups.delete_group_usecase import DeleteGroupUsecase
from app.src.application.usecases.strategies.create_strategies_usecase import CreateStrategiesUsecase
from app.src.application.usecases.strategies.read_strategies_usecase import ReadStrategiesUsecase

from app.src.application.usecases.user.create_user import CreateUserUsecase
from app.src.application.usecases.user.get_user import ReadUserUsecase
from app.src.application.usecases.user.update_user import UpdateUserUsecase
from app.src.application.usecases.user.delete_user import DeleteUserUsecase
from app.src.application.usecases.connections.create_connection_usecase import CreateConnectionUsecase
from app.src.application.usecases.groups.get_groups_usecase import GetGroupsUsecase
from app.src.application.usecases.groups.create_group_usecase import CreateGroupUsecase

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
        strategies_repository = StrategiesRepository(session=session)

        create_user = CreateUserUsecase(user_repository)
        read_user = ReadUserUsecase(user_repository, conn_repository, organization_repository=org_repo)
        update_user = UpdateUserUsecase(user_repository)
        delete_user = DeleteUserUsecase(user_repository)
        self.user_controller = UserController(create_user=create_user, get_user=read_user, update_user=update_user, delete_user=delete_user)

        create_conn_usecase = CreateConnectionUsecase(conn_repository, user_repository, groups_has_users)
        read_conn_usecase = ReadConnectionsUsecase(conn_repository=conn_repository)
        delete_conn_usecase = DeleteConnectionsUsecase(conn_repository=conn_repository)
        self.connection_controller = ConnectionController(create_connection=create_conn_usecase,
                                                          read_connections=read_conn_usecase,
                                                          delete_connections=delete_conn_usecase)

        get_groups_usecase = GetGroupsUsecase(group_has_user_repository=groups_has_users,
                                              groups_repository=groups_repository,
                                              user_repository=user_repository)
        create_group_usecase = CreateGroupUsecase(groups_has_users_repository=groups_has_users,
                                                  groups_repository=groups_repository,
                                                  users_repository=user_repository)
        delete_groups_usecase = DeleteGroupUsecase(groups_repository=groups_repository)
        self.groups_controller = GroupsController(get_groups_usecase=get_groups_usecase, 
                                                  create_group_usecase=create_group_usecase,
                                                  delete_group_usecase=delete_groups_usecase)

        create_strategys_usecase = CreateStrategiesUsecase(strategies_repository=strategies_repository)
        read_strategies = ReadStrategiesUsecase(strategies_repository=strategies_repository)
        self.strategies_controller = StrategiesController(create_strategies_usecase=create_strategys_usecase,
                                                          read_strategies_usecase=read_strategies)