from sqlalchemy.orm import Session

from app.src.domain.interfaces.strategies_repository_interface import StrategiesRepositoryInterface
from app.src.infra.models.strategies_model import StrategiesModel

class StrategiesRepository(StrategiesRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create(self,
               organization_id: int,
               name: str,
               content: str):
        try:
            strategy = StrategiesModel(organization_id=organization_id,
                                       name=name,
                                       content=content)

            self.__session.add(strategy)
            self.__session.commit()
            return strategy
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError (f"Erro ao criar connection: {e}")

    def get_all(self):
        try:
            strategies = self.__session.query(StrategiesModel).filter_by(organization_id=1)
            if not strategies:
                return None
            return strategies
        except Exception as e:
            raise RuntimeError(e)

    def delete(self, id: int):
        try:
            strategy = self.__session.query(StrategiesModel).filter_by(id = id).first()
            if strategy:
                self.__session.delete(strategy)
                self.__session.commit()
            return None
        except Exception as e:
            raise e

    def update(self, id:int, name: str, content: dict):
        try:
            strategy = self.__session.query(StrategiesModel).filter_by(id=id).first()

            if strategy:
                strategy.name = name
                strategy.content = content

                self.__session.commit()

            return None
        except Exception as e:
            self.__session.rollback()
            raise e

    def get_by_id(self, id: int) -> list:
        try:
            strategies = self.__session.query(StrategiesModel).filter_by(id=id).first()
            if not strategies:
                return None
            return strategies
        except Exception as e:
            raise RuntimeError(e)
