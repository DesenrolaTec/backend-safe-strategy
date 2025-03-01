from app.src.domain.interfaces.connection_repository_interface import ConnectionRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface


class DeleteConnectionsUsecase(UseCaseInterface):
    def __init__(self,
                 conn_repository: ConnectionRepositoryInterface):
        self.conn_repository = conn_repository

    def execute(self, conn_id: int, user_id: int):
        try:
            self.conn_repository.delete(conn_id=conn_id, user_id = user_id)
            return None
        except Exception as e:
            raise e