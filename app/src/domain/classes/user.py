from typing import Optional
from datetime import datetime
from app.src.domain.classes.validator import Validator

class User:
    def __init__(self,
                id: Optional[int] = None,
                name: Optional[str] = None,
                email: Optional[str] = None,
                password: Optional[str] = None,
                cpf: Optional[str] = None,
                birthday: Optional[str] = None,
                created_at: Optional[str] = None,
                updated_at: Optional[str] = None):
        self._id = id
        self._name = name
        self._email = email
        self._password = password
        self._cpf = cpf
        self._birthday = birthday
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]):
        self._id = value

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]):
        self._name = value

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, value: Optional[str]):
        self._email = Validator.ensure_valid_email(value) if value else None

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, value: Optional[str]):
        self._password = Validator.ensure_password_secure(value) if value else None

    @property
    def cpf(self) -> Optional[str]:
        return self._cpf

    @cpf.setter
    def cpf(self, value: Optional[str]):
        self._cpf = Validator.ensure_valid_cpf(value) if value else None

    @property
    def birthday(self) -> Optional[str]:
        return self._birthday

    @birthday.setter
    def birthday(self, value: Optional[str]):
        self._birthday = Validator.ensure_valid_birthday(value) if value else None

    @property
    def created_at(self) -> Optional[str]:
        return self._created_at

    @created_at.setter
    def created_at(self, value: Optional[str]):
        self._created_at = value

    @property
    def updated_at(self) -> Optional[str]:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: Optional[str]):
        self._updated_at = value

    def __str__(self):
        return (f'User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, '
                f'cpf={self.cpf}, birthday={self.birthday}, created_at={self.created_at}, updated_at={self.updated_at})')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'cpf': self.cpf,
            'birthday': self.birthday,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }