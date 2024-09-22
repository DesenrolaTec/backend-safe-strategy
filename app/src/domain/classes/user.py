import re
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
        soma = sum(int(digito) * peso for peso, digito in enumerate(cpf_parcial, start=2))
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
    def ensure_valid_birthday(birthday: str) -> str:
        try:
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise InvalidBirthdayError(BIRTHDAY_FORMAT_INVALID)

        today = datetime.today()
        age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
        if age < 18:
            raise InvalidBirthdayError(UNDERAGE_ERROR)
        return birthday_date.strftime('%Y-%m-%d')


class User:
    def __init__(self, name: str, email: str, password: str, cpf: str, birthday: str) -> None:
        self.__name: str = name
        self.__email: str = Validator.ensure_valid_email(email=email)
        self.__password: str = Validator.ensure_password_secure(password=password)
        self.__cpf: Final[str] = Validator.ensure_valid_cpf(cpf=cpf)
        self.__birthday: Final[str] = Validator.ensure_valid_birthday(birthday=birthday)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = Validator.ensure_valid_email(value)
    
    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        self.__password = Validator.ensure_password_secure(password=value)
    
    @property
    def cpf(self) -> str:
        return self.__cpf
    
    @property
    def birthday(self) -> str:
        return self.__birthday
