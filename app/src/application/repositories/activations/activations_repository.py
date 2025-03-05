from sqlalchemy.orm import Session

from app.src.domain.interfaces.activations_repository_interface import ActivationsRepositoryInterface
from app.src.infra.models.activations_model import ActivationsModel

class ActivationsRepository(ActivationsRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def read_id(self, activation_id: int):
        try:
            activations = self.__session.query(ActivationsModel).filter_by(id=activation_id)
            if activations:
                return activations
            return None
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError (f"Erro ao criar connection: {e}")