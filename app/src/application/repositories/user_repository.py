from sqlalchemy.orm import Session
from app.src.domain.classes.user import User
from app.src.domain.factorys.user_factory import UserDto, user_client
from app.src.domain.factorys.user_factory import user_client, FullUserFactory, MinimalUserFactory
from app.src.infra.models.user_model import UserModel
from app.src.infra.models.token_model import OAuth2Token
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session
        self._minimal_user_factory = MinimalUserFactory()
        self._full_user_factory = FullUserFactory()

    def create(self, user: UserDto, is_minimal_user: bool = False) -> User:
        if is_minimal_user:            
            user = user_client(self._minimal_user_factory, user)
        else:
            user = user_client(self._full_user_factory, user)

        user_model = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
            cpf=user.cpf,
            birthday=user.birthday
        )
        try:
            self.__session.add(user_model)
            self.__session.commit()
            db_user = self.get_by_cpf(user_model.cpf)
            return db_user
        except Exception as e:
            self.__session.rollback()
            raise Exception(f"Erro ao criar usuário: {str(e)}")
        
    def get_by_id(self, user_id: int) -> UserModel:
        db_user = self.__session.query(UserModel).filter_by(id=user_id).first()
        if not db_user:
            return None
        return db_user

    def get_by_cpf(self, user_cpf: str) -> UserModel:
        db_user = self.__session.query(UserModel).filter_by(cpf=user_cpf).first()
        if not db_user:
            return None
        return db_user
    
    def get_by_email(self, user_email: str) -> User:
        db_user = self.__session.query(UserModel).filter_by(email=user_email).first()
        if not db_user:
            return None
        return db_user

    def update(self, user_dto: UserDto) -> User|dict:
        db_user = self.get_by_cpf(user_dto.cpf)
        if db_user:
            user = user_client(self._full_user_factory, user_dto)
            try:
                db_user.name = user.name
                db_user.email = user.email
                db_user.cpf = user.cpf
                db_user.password = user.password
                db_user.birthday = user.birthday
                self.__session.commit()
                return user
            except Exception as e:
                self.__session.rollback()  
                return {'error': f'Error updating user: {str(e)}'}            
        return {'error': 'Usuario não encontrado.'}

    def update_conn(self, user_dto, user_id) -> int:
        db_user = self.get_by_id(user_id)
        if db_user:
            try:
                db_user.name = user_dto.user_name
                db_user.email = user_dto.user_email
                db_user.cpf = user_dto.user_cpf
                self.__session.commit()
                return db_user.id
            except Exception as e:
                self.__session.rollback()
                return {'error': f'Error updating user: {str(e)}'}
        return {'error': 'Usuario não encontrado.'}

    def delete(self, user_cpf: str) -> str:
        user = self.__session.query(UserModel).filter_by(cpf=user_cpf).first()
        if user:
            try:
                self.__session.query(OAuth2Token).filter_by(user_id=user.id).delete()
                self.__session.commit()
                self.__session.delete(user)
                self.__session.commit()
                user = user_client(self._minimal_user_factory, user)
                return user
            except Exception as e:
                self.__session.rollback()  # Rollback em caso de erro
                return f'Error deleting user: {str(e)}'
        else:
            return 'User not found.'

    def delete_by_id(self, id: str) -> str:
        user = self.__session.query(UserModel).filter_by(id=id).first()
        if user:
            try:
                self.__session.query(OAuth2Token).filter_by(user_id=user.id).delete()
                self.__session.commit()
                self.__session.delete(user)
                self.__session.commit()
                user = user_client(self._minimal_user_factory, user)
                return user
            except Exception as e:
                self.__session.rollback()  # Rollback em caso de erro
                return f'Error deleting user: {str(e)}'
        else:
            return 'User not found.'