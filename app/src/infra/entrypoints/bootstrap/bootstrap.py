from app.src.application.controllers.user_controller import UserController
from app.src.application.controllers.connection_controller import ConnectionController

from app.src.application.usecases.user.create_user import CreateUserUsecase
from app.src.application.usecases.user.get_user import ReadUserUsecase
from app.src.application.usecases.user.update_user import UpdateUserUsecase
from app.src.application.usecases.user.delete_user import DeleteUserUsecase
from app.src.application.usecases.connections.create_connection_usecase import CreateConnectionUsecase

from app.src.application.repositories.user_repository import UserRepository
from app.src.application.repositories.connection_repository import ConnectionRepository

from app.src.infra.adapters.sql_alchemy_adapter import db

class Bootstrap:
    def __init__(self):
        self.load_dependencies()

    def load_dependencies(self):
        session = db.session
        user_repository = UserRepository(session)
        create_user = CreateUserUsecase(user_repository)
        read_user = ReadUserUsecase(user_repository)
        update_user = UpdateUserUsecase(user_repository)
        delete_user = DeleteUserUsecase(user_repository)
        self.user_controller = UserController(create_user=create_user, get_user=read_user, update_user=update_user, delete_user=delete_user)

        conn_repository = ConnectionRepository(session)
        conn_usecase = CreateConnectionUsecase(conn_repository, user_repository)
        self.connection_controller = ConnectionController(conn_usecase)