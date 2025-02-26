from app.src.domain.interfaces.connection_controller_interface import ConnectionControllerInterface
from app.src.application.usecases.connections.create_connection_usecase import CreateConnectionUsecase, InputDto as CreateConnectionInputDto
from app.src.application.usecases.connections.read_connections_usecase import ReadConnectionsUsecase

class ConnectionController(ConnectionControllerInterface):
    def __init__(self,
                 create_connection: CreateConnectionUsecase,
                 read_connections: ReadConnectionsUsecase)->None:
        self._create_connection = create_connection
        self._read_connection = read_connections

    def _map_connection_data_create(self, connection_data: dict)->any:
        return CreateConnectionInputDto(user_name= connection_data.get("user_name"),
                                        user_email= connection_data.get("user_email"),
                                        user_cpf= connection_data.get("user_cpf"),
                                        user_client_code= connection_data.get("user_client_code"),
                                        user_enable= connection_data.get("user_enable"),
                                        user_groups_ids= connection_data.get("user_groups_ids"))

    def create_connection(self, conn_data: dict):
        conn_dto = self._map_connection_data_create(conn_data)
        output_dto = self._create_connection.execute(conn_dto)
        return output_dto.__dict__

    def read_connections(self) -> list:
        try:
            response = []
            results = self._read_connections.execute()
            for result in results:
                response.append(result.__dict__)
            return response
        except Exception as e:
            return e