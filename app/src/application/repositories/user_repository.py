from sqlalchemy.orm import Session
from app.src.domain.classes.user import User
from app.src.domain.factorys.user_factory import UserDto
from app.src.domain.factorys.user_factory import user_client, FullUserFactory, MinimalUserFactory
from app.src.infra.models.user_model import UserModel, user_client
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session
        self._minimal_user_factory = MinimalUserFactory()
        self._full_user_factory = FullUserFactory()

    def create(self, user: UserDto) -> User:
        if user.cpf == "":            
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
            return user
        except Exception as e:
            self.__session.rollback()
            raise Exception(f"Erro ao criar usuário: {str(e)}")

    def get_by_cpf(self, user_cpf: str) -> User:
        db_user = self.__session.query(UserModel).filter_by(cpf=user_cpf).first()
        user = user_client(self._minimal_user_factory, db_user)
        if user.cpf:
            return user
        return None
    
    def get_by_email(self, user_email: str) -> User:
        db_user = self.__session.query(UserModel).filter_by(email=user_email).first()
        user = user_client(self._minimal_user_factory, db_user)
        if user.cpf:
            return user
        return None

    def update(self, user_cpf: str, user: UserDto) -> User|dict:
        user = self.get_by_cpf(user_cpf)
        if user:
            user = user_client(self._minimal_user_factory, user)
            try:
                user.name = user.name
                user.email = user.email
                user.password = user.password
                user.birthday = user.birthday
                self.__session.commit()
                return user
            except Exception as e:
                self.__session.rollback()  
                return {'error': f'Error updating user: {str(e)}'}
        else:
            return {'error': 'User not found.'}

    def delete(self, user_cpf: str) -> str:
        user = self.__find_user_by_cpf(user_cpf)
        if user:
            try:
                self.__session.delete(user)
                self.__session.commit()
                return 'User deleted successfully.'
            except Exception as e:
                self.__session.rollback()  # Rollback em caso de erro
                return f'Error deleting user: {str(e)}'
        else:
            return 'User not found.'