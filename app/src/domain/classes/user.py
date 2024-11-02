import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final
from datetime import datetime
from app.src.application.exceptions.user_exceptions import (InvalidBirthdayError,
                                                        InvalidCPFError,
                                                        InvalidEmailError,
                                                        WeakPasswordError)

# Constantes de erro
EMAIL_IS_NOT_VALID = "Email is not valid"
EMAIL_TOO_LONG = "Email is too long"
INVALID_CPF = "Invalid CPF"
PASSWORD_TOO_SHORT = "Password must be at least 8 characters long."
PASSWORD_NO_UPPERCASE = "Password must contain at least one uppercase letter."
PASSWORD_NO_LOWERCASE = "Password must contain at least one lowercase letter."
PASSWORD_NO_DIGIT = "Password must contain at least one digit."
PASSWORD_NO_SPECIAL_CHAR = "Password must contain at least one special character."
BIRTHDAY_FORMAT_INVALID = "Birthday format must be YYYY-MM-DD"
UNDERAGE_ERROR = "Person must be at least 18 years old."

class Validator:
    @staticmethod
    def ensure_valid_email(email: str) -> str:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if len(email) > 254:
            raise InvalidEmailError(EMAIL_TOO_LONG)
        if not re.match(pattern, email):
            raise InvalidEmailError(EMAIL_IS_NOT_VALID)
        return email
    
    @staticmethod
    def calcular_digito_verificador(cpf_parcial: str) -> int:
        if len(cpf_parcial) == 9:
            multiplicadores = list(range(10, 1, -1))
        elif len(cpf_parcial) == 10:
            multiplicadores = list(range(11, 1, -1))
        else:
            raise ValueError("CPF parcial inválido. Deve conter 9 ou 10 dígitos.")

        soma = sum(int(digito) * multiplicador for digito, multiplicador in zip(cpf_parcial, multiplicadores))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    @staticmethod
    def ensure_valid_cpf(cpf: str) -> str:
        cpf = cpf.replace(".", "").replace("-", "")
        if len(cpf) != 11 or not cpf.isdigit():
            raise InvalidCPFError(INVALID_CPF)
        
        if cpf == cpf[0] * 11:
            raise InvalidCPFError(INVALID_CPF)

        primeiro_digito = Validator.calcular_digito_verificador(cpf[:9])
        if primeiro_digito != int(cpf[9]):
            raise InvalidCPFError(INVALID_CPF)

        segundo_digito = Validator.calcular_digito_verificador(cpf[:10])
        if segundo_digito != int(cpf[10]):
            raise InvalidCPFError(INVALID_CPF)

        return cpf

    @staticmethod
    def ensure_password_secure(password: str) -> str:
        if len(password) < 8:
            raise WeakPasswordError(PASSWORD_TOO_SHORT)
        if not re.search(r'[A-Z]', password):
            raise WeakPasswordError(PASSWORD_NO_UPPERCASE)
        if not re.search(r'[a-z]', password):
            raise WeakPasswordError(PASSWORD_NO_LOWERCASE)
        if not re.search(r'[0-9]', password):
            raise WeakPasswordError(PASSWORD_NO_DIGIT)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise WeakPasswordError(PASSWORD_NO_SPECIAL_CHAR)

        return password

    @staticmethod
    def ensure_valid_birthday(birthday: str) -> datetime:
        try:
            if not type(birthday) == datetime:
                birthday = datetime.strptime(birthday, '%Y-%m-%d')            
        except ValueError:
            raise InvalidBirthdayError(BIRTHDAY_FORMAT_INVALID)

        today = datetime.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if age < 18:
            raise InvalidBirthdayError(UNDERAGE_ERROR)
        return birthday.strftime('%Y-%m-%d')

class User:
    def __init__(self, email: str, name: str, password: str, cpf: str, birthday: str)->None:
        self.email = email
        self.name = name
        self.password = password
        self.cpf = cpf
        self.birthday = birthday

    def __dict__(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "cpf": self.cpf,
            "birthday": self.birthday
        }

@dataclass
class UserDto:
    email: str
    name: str=""
    password: str=""
    cpf: str=""
    birthday: str=""

class UserFactory:
    @abstractmethod
    def create_user(self)->User:
        pass

class MinimalUserFactory(UserFactory):
    def create_user(self, email: str, name: str="", password: str="", cpf: str="", birthday: str="") -> User:
        return User(email=email, name=name, password=password, cpf=cpf, birthday=birthday)
    
class FullUserFactory(UserFactory):
    def create_user(self, email: str, name: str, password: str, cpf: str, birthday: str) -> User:
        self.name = name 
        self.email = Validator.ensure_valid_email(email=email) 
        self.password = Validator.ensure_password_secure(password=password)
        self.cpf = Validator.ensure_valid_cpf(cpf=cpf)
        self.birthday = Validator.ensure_valid_birthday(birthday=birthday)
        return User(name=self.name, email= self.email, password= self.password, cpf=self.cpf, birthday=self.birthday)

def user_client(factory: UserFactory, user_dto: UserDto):
    user = factory.create_user(email=user_dto.email, 
                               name=user_dto.name, 
                               password=user_dto.password, 
                               cpf=user_dto.cpf, 
                               birthday=user_dto.birthday)
    return user