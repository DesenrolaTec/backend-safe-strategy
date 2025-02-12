from sqlalchemy.orm import Session
from app.src.domain.classes.groups.dto import GroupsDto
from app.src.infra.models.groups_model import GroupsModel
from app.src.domain.interfaces.groups_repository_interface import IgroupsRepository

def map_groups_dto(model: GroupsModel)->GroupsDto:
    return GroupsDto(id=model.id,
                     organization_id=model.organization_id,
                     name=model.name,
                     created_at=model.created_at,
                     updated_at=model.updated_at)

class GroupsRepository(IgroupsRepository):
    def __init__(self, session: Session):
        self.__session = session

    def get_groups_by_organization(self, organization_id: int)->list[GroupsDto]:
        try:
            result = []
            groups = self.__session.query(GroupsModel).filter_by(organization_id=organization_id)
            for group in groups:
                group_dto = map_groups_dto(group)
                result.append(group_dto)
            return groups
        except Exception as e:
            raise RuntimeError(f"Erro ao recuperar grupos.: {e}")

    def get_group_by_name(self, group_name: str) -> GroupsDto:
        try:
            group = self.__session.query(GroupsModel).filter_by(name=group_name).first()
            group_dto = map_groups_dto(group)
            return group_dto
        except Exception as e:
            raise RuntimeError(f"Erro ao recuperar grupo pelo nome.: {e}")

    def create_group(self, group_name: str, organization_id: int) -> None:
        try:
            groups_model = GroupsModel(name = group_name,
                                       organization_id = organization_id)
            self.__session.add(groups_model)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError(f"Erro ao criar o grupo {e}")



