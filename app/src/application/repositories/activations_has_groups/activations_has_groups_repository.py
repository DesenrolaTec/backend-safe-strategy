from sqlalchemy.orm import Session
from app.src.domain.interfaces.activations_has_groups_repository import ActivationsHasGroupsRepository
from app.src.infra.models.activations_has_groups import ActivationsHasGroupsModel

class ActivationsHasGroupsRepository(ActivationsHasGroupsRepository):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def read_activations_by_group(self, groups_id: int) -> list:
        try:
            activations = self.__session.query(ActivationsHasGroupsModel).filter_by(groups_id=groups_id)
            if activations:
                return activations
            return None
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError (f"Erro ao criar connection: {e}")