from sqlalchemy.orm import Session
from app.src.domain.classes.user import User
from app.src.infrastructure.models.user_model import UserModel
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create(self, user: User) -> User:
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
            return user  # Retorna o objeto criado
        except Exception as e:
            self.__session.rollback()  # Rollback em caso de erro
            raise Exception(f"Erro ao criar usuário: {str(e)}")

    def get_by_id(self, user_cpf: str) -> User:
        user = self.__find_user_by_cpf(user_cpf)
        if user:
            return User(
                name=user.name,
                email=user.email,
                password=user.password,
                cpf=user.cpf,
                birthday=user.birthday
            )
        return None
    
    def __find_user_by_email(self, user_email: str) -> UserModel:
        return self.__session.query(UserModel).filter_by(email=user_email).first()
    
    def get_by_email(self, user_email: str) -> User:
        user = self.__find_user_by_email(user_email)
        if user:
            return User(
                name=user.name,
                email=user.email,
                password=user.password,
                cpf=user.cpf,
                birthday=user.birthday
            )
        return None

    def update(self, user_cpf: str, data: dict) -> dict:
        user = self.__find_user_by_cpf(user_cpf)
        if user:
            try:
                user.name = data.get("name", user.name)
                user.email = data.get("email", user.email)
                user.password = data.get("password", user.password)
                user.birthday = data.get("birthday", user.birthday)
                self.__session.commit()
                return {'message': 'User updated successfully.'}, 200
            except Exception as e:
                self.__session.rollback()  # Rollback em caso de erro
                return {'error': f'Error updating user: {str(e)}'}, 500
        else:
            return {'error': 'User not found.'}, 404

    def delete(self, user_cpf: str) -> dict:
        user = self.__find_user_by_cpf(user_cpf)
        if user:
            try:
                self.__session.delete(user)
                self.__session.commit()
                return {'message': 'User deleted successfully.'}, 204
            except Exception as e:
                self.__session.rollback()  # Rollback em caso de erro
                return {'error': f'Error deleting user: {str(e)}'}, 500
        else:
            return {'error': 'User not found.'}, 404

    def __find_user_by_cpf(self, user_cpf: str) -> UserModel:
        return self.__session.query(UserModel).filter_by(cpf=user_cpf).first()
