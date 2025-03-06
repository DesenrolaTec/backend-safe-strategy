from sqlalchemy.orm import Session
from app.src.domain.interfaces.activations_has_groups_repository import ActivationsHasGroupsRepositoryInterface
from app.src.infra.models.activations_has_groups import ActivationsHasGroupsModel

class ActivationsHasGroupsRepository(ActivationsHasGroupsRepositoryInterface):
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

    def read_activations_by_id(self, id: int):
        try:
            activations = self.__session.query(ActivationsHasGroupsModel).filter_by(activations_id=id).all()
            if activations:
                return activations
            return None
        except Exception as e:
            raise e

    def insert(self, activation_id: int, group_id: int):
        try:
            act_h_g = ActivationsHasGroupsModel(
                activations_id=activation_id,
                groups_id=group_id
            )
            self.__session.add(act_h_g)
            self.__session.commit()
            return None
        except Exception as e:
            self.__session.rollback()
            raise e