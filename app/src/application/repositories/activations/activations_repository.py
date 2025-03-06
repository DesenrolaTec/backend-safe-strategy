from sqlalchemy.orm import Session
from app.src.domain.interfaces.activations_repository_interface import ActivationsRepositoryInterface
from app.src.infra.models.activations_model import ActivationsModel
from dataclasses import dataclass

@dataclass
class ActivationDto:
    organization_id: int
    strategy_id: int
    start_at: str
    stop_at: str
    file_url: str

class ActivationsRepository(ActivationsRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def read_id(self, activation_id: int):
        try:
            activations = self.__session.query(ActivationsModel).filter_by(id=activation_id).first()
            if activations:
                return activations
            return None
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError (f"Erro ao criar connection: {e}")

    def read_all(self):
        try:
            activations = self.__session.query(ActivationsModel).all()
            if activations:
                return activations
            return None
        except Exception as e:
            raise e

    def create(self, data: ActivationDto):
        try:
            activation = ActivationsModel(
                organization_id=data.organization_id,
                strategy_id=data.strategy_id,
                start_at=data.start_at,
                stop_at=data.stop_at,
                file_url=data.file_url
            )
            self.__session.add(activation)
            self.__session.flush()
            self.__session.commit()

            return activation
        except Exception as e:
            self.__session.rollback()
            raise e