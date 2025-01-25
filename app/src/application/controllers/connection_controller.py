from app.src.domain.interfaces.connection_controller_interface import ConnectionControllerInterface
from app.src.application.usecases.connections.create_connection_usecase import CreateConnectionUsecase, InputDto as CreateConnectionInputDto

class ConnectionController(ConnectionControllerInterface):
    def __init__(self, create_connection: CreateConnectionUsecase)->None:
        self._create_connection = create_connection

    def _map_connection_data_create(self, connection_data: dict)->any:
        return CreateConnectionInputDto(email = connection_data['user_email'], organization_id = connection_data['organization_id'], role = connection_data['role'])

    def create_connection(self, conn_data: dict):
        conn_dto = self._map_connection_data_create(conn_data)
        output_dto = self._create_connection.execute(conn_dto)
        return output_dto.__dict__