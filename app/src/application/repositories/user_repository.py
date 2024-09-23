from sqlalchemy.orm import Session
from app.src.domain.classes.user import User
from app.src.infrastructure.models.user_model import UserModel
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session)->None:
        self.__session = session

    def create(self, user: User)->None:
        user_model = UserModel(name = user.name,
                               email = user.email,
                               password = user.password,
                               cpf = user.cpf,
                               birthday = user.birthday)
        self.__session.add(user_model)
        self.__session.commit()

    def get_by_id(self, user_cpf: str)->User:
        user = self.__session.query(UserModel).filter_by(cpf=user_cpf).first()
        if user:
            return User(name = user.name,
                        email = user.email,
                        password = user.password,
                        cpf = user.cpf,
                        birthday = user.birthday)
        return None
    
    def update(self, user_cpf: str, data: dict)->dict:
        user = self.__session.query(UserModel).filter_by(cpf=user_cpf).first()
        if user:
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)
            user.password = data.get("password", user.password)
            user.birthday = data.get("birthday", user.birthday)
            self.__session.commit()  # Confirma a transação
            return {'message': 'User deleted successfully.'}, 204  # 204 No Content
        else:
            return {'error': 'User not found.'}, 404  # 404 Not Found
        
    def delete(self, user_cpf: str)->dict:
        user = self.__session.query(UserModel).filter_by(cpf=user_cpf).first()
        if user:
            self.__session.delete(user)  # Deleta o objeto
            self.__session.commit()  # Confirma a transação
            return {'message': 'User deleted successfully.'}, 204  # 204 No Content
        else:
            return {'error': 'User not found.'}, 404  # 404 Not Found
        
    


    