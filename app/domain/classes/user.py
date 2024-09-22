import re
from datetime import datetime
from application.exceptions.user_exceptions import InvalidBirthdayError

class User():
    def __ensure_valid_email(self, email: str)->str:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if len(email) > 254:
            raise ValueError("Email is too long")
        if re.match(pattern, email):
            return email
        else:
            raise ValueError("Email is not valid")

    def __ensure_valid_cpf(self, cpf: str) -> str:
        cpf = cpf.replace(".", "").replace("-", "")
        
        if not (cpf.isdigit() and len(cpf) == 11):
            raise ValueError(f"Invalid CPF: {cpf}")

        if cpf == cpf[0] * 11:
            raise ValueError(f"Invalid CPF: {cpf}")

        def calcular_digito(cpf_parcial: str) -> int:
            peso = len(cpf_parcial) + 1
            soma = sum(int(digito) * peso for peso, digito in enumerate(cpf_parcial, start=2))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        primeiro_digito = calcular_digito(cpf[:9])
        if primeiro_digito != int(cpf[9]):
            raise ValueError(f"Invalid CPF: {cpf}")
        
        segundo_digito = calcular_digito(cpf[:10])
        if segundo_digito != int(cpf[10]):
            raise ValueError(f"Invalid CPF: {cpf}")
        
        return cpf
    
    def __ensure_password_secure(self, password: str):
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

    def __ensure_valid_birthday(self, birthday: str):
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if age < 18:
            raise InvalidBirthdayError("Person must be at least 18 years old.")
        return birthday.strftime('%Y-%m-%d')

    def __init__(self, name: str, email: str, password: str, cpf: str, birthday: datetime)->None:
        self.__name = name
        self.__email = self.__ensure_valid_email(email=email)
        self.__password = self.__ensure_password_secure(password=password)
        self.__cpf = self.__ensure_valid_cpf(cpf=cpf)
        self.__birthday = self.__ensure_valid_birthday(birthday=birthday)
        