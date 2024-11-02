from sqlalchemy.orm import Session
from app.src.domain.dtos.profile_dto import ProfileDto
from app.src.infrastructure.models.profiles_model import ProfilesModel
from app.src.domain.interfaces.profiles_repository_interface import ProfilesRepositoryInterface

class ProfilesRepository(ProfilesRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create(self, connetion: ProfileDto) -> ProfileDto:
        profile_model = ProfilesModel(
            user_id = connetion.user_id,
            organization_id = connetion.organization_id,
            name = connetion.name,
            enable = connetion.enable
        )
        try:
            self.__session.add(profile_model)
            self.__session.commit()
            return connetion  # Retorna o objeto criado
        except Exception as e:
            self.__session.rollback()  # Rollback em caso de erro
            raise Exception(f"Erro ao criar connection: {str(e)}")
        
    def __find_connections_by_organization(self, organization_id: int) -> list[ProfilesModel]:
        return self.__session.query(ProfilesModel).filter_by(organization_id=organization_id).first()

    def get_profiles_by_organization(self, organization_id: int) -> list:
        profiles = self.__find_connections_by_organization(organization_id)
        profiles_list = []
        if profiles:
            for profile in profiles:
                profiles_list.append(
                    ProfileDto(
                        user_id=profile.user_id,
                        organization_id=profile.organization_id,
                        name=profile.name,
                        enable=profile.enable
                    )
                )
            return profiles_list
        return None