from sqlalchemy.orm import Session
from app.src.domain.classes.user import User
from app.src.infrastructure.models.user_model import UserModel
from app.src.domain.interfaces.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session)->None:
        self.session = session

    def create(self, user: User)->None:
        user_model = UserModel(name = user.name,
                               email = user.email,
                               password = user.password,
                               cpf = user.cpf,
                               birthday = user.birthday)
        self.session.add(user_model)
        self.session.commit()

    def get_by_id(self, user_cpf: str)->User:
        user_model = self.session.query(UserModel).filter_by(cpf=user_cpf).first()
        if user_model:
            return User(name = user_model.name,
                        email = user_model.email,
                        password = user_model.password,
                        cpf = user_model.cpf,
                        birthday = user_model.birthday)
        return None

    