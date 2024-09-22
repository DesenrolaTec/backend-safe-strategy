import re
from typing import Optional
from datetime import datetime
from app.application.exceptions.user_exceptions import InvalidBirthdayError

EMAIL_IS_NOT_VALID = "Email is not valid"
EMAIL_TOO_LONG = "Email is too long"
INVALID_CPF = "Invalid CPF"

class Validator:
    @staticmethod
    def ensure_valid_email(email: str) -> str:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if len(email) > 254:
            raise ValueError(EMAIL_TOO_LONG)
        if not re.match(pattern, email):
            raise ValueError(EMAIL_IS_NOT_VALID)
        return email

    @staticmethod
    def ensure_valid_cpf(cpf: str) -> str:
        cpf = cpf.replace(".", "").replace("-", "")
        
        if not (cpf.isdigit() and len(cpf) == 11):
            raise ValueError(f"{INVALID_CPF}: {cpf}")

        if cpf == cpf[0] * 11:
            raise ValueError(f"{INVALID_CPF}: {cpf}")
        
        return cpf
    
    @staticmethod
    def ensure_password_secure(password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character.")

        return password

    @staticmethod
    def ensure_valid_birthday(birthday: str):
        try:
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Birthday format must be YYYY-MM-DD")

        today = datetime.today()
        age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
        if age < 18:
            raise InvalidBirthdayError("Person must be at least 18 years old.")
        return birthday_date.strftime('%Y-%m-%d')

class User():
    def __init__(self, name: str, email: str, password: str, cpf: str, birthday: str)->None:
        self.__name: str = name
        self.__email: str = Validator.ensure_valid_email(email=email)
        self.__password: str = Validator.ensure_password_secure(password=password)
        self.__cpf: str = Validator.ensure_valid_cpf(cpf=cpf)
        self.__birthday: str = Validator.ensure_valid_birthday(birthday=birthday)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> Optional[str]:
        self.__name = value
        return self.__email

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> Optional[str]:
        self.__email = Validator.ensure_valid_email(value)
        return self.__email
    
    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str) -> Optional[str]:
        self.__password = Validator.ensure_password_secure(password=value)
        return self.__password
    
    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, value: str) -> Optional[str]:
        self.__cpf = Validator.ensure_valid_cpf(cpf=value)
        return self.__cpf
    
    @property
    def birthday(self) -> str:
        return self.__birthday

    @birthday.setter
    def birthday(self, value: str) -> Optional[str]:
        self.__birthday = Validator.ensure_valid_birthday(birthday=value)
        return self.__birthday