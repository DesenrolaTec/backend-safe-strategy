from typing import Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from app.src.domain.classes.user import User
from app.src.domain.classes.validator import Validator

@dataclass
class UserDto:
    id: Optional[int] = None 
    name: Optional[str] = None 
    email: Optional[str] = None 
    password: Optional[str] = None 
    cpf: Optional[str] = None 
    birthday: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserFactory(ABC):
    @abstractmethod
    def create_user(self, user_dto: UserDto) -> User:
        pass

class MinimalUserFactory(UserFactory):
    def create_user(self, user_dto: UserDto) -> User:
        return User(email=user_dto.email, name=user_dto.name, password=user_dto.password, cpf=user_dto.cpf, birthday=user_dto.birthday)

class FullUserFactory(UserFactory):
    def create_user(self, user_dto: UserDto) -> User:
        email = Validator.ensure_valid_email(user_dto.email)
        password = Validator.ensure_password_secure(user_dto.password)
        cpf = Validator.ensure_valid_cpf(user_dto.cpf)
        birthday = Validator.ensure_valid_birthday(user_dto.birthday)
        return User(name=user_dto.name, email=email, password=password, cpf=cpf, birthday=birthday)

def user_client(factory: UserFactory, user_dto: UserDto):
    user = factory.create_user(user_dto)
    return user

                 