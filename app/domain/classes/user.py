from datetime import datetime

class User():
    def __is_valid_email(self, email: str):
        """
            Validates the given email address.

            This method checks if the email conforms to standard email formatting rules.
            It uses a regular expression to ensure the email:
            - Contains a valid username part (alphanumeric characters, underscores, dots, percentages, pluses, and hyphens).
            - Includes an '@' symbol followed by a valid domain name.
            - Ends with a top-level domain (TLD) that consists of at least two alphabetic characters.
            
            Additionally, it ensures that the email length does not exceed 254 characters.

            Args:
                email (str): The email address to validate.

            Returns:
                str: The validated email address if it is valid.

            Raises:
                ValueError: If the email is invalid or exceeds the length limit.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if len(email) > 254:
            raise ValueError("Email muito longo")
        if re.match(pattern, email):
            return email
        else:
            raise ValueError("Email inválido")

    def __is_cpf_valid(self, cpf: str) -> bool:
        """
            Validates the given CPF (Cadastro de Pessoas Físicas) number.

            This method checks if the CPF is valid according to Brazilian CPF validation rules.
            It verifies that the CPF consists of exactly 11 digits, and performs a series of
            calculations to ensure that the check digits are correct.

            Args:
                cpf (str): The CPF number to validate.

            Returns:
                bool: True if the CPF is valid, False otherwise.

            Raises:
                ValueError: If the CPF contains non-numeric characters or is not exactly 11 digits.
        """
        cpf = cpf.replace(".", "").replace("-", "")
        
        if not (cpf.isdigit() and len(cpf) == 11):
            return False

        if cpf == cpf[0] * 11:
            return False

        def calcular_digito(cpf_parcial: str) -> int:
            peso = len(cpf_parcial) + 1
            soma = sum(int(digito) * peso for peso, digito in enumerate(cpf_parcial, start=2))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        primeiro_digito = calcular_digito(cpf[:9])
        if primeiro_digito != int(cpf[9]):
            return False
        
        segundo_digito = calcular_digito(cpf[:10])
        if segundo_digito != int(cpf[10]):
            return False
        
        return True
    
    def __is_password_secure(self, password: str):
        """
        Validates the security of the given password.

        This method checks if the password meets specific security criteria:
        - Minimum length of 8 characters.
        - At least one uppercase letter.
        - At least one lowercase letter.
        - At least one digit.
        - At least one special character (e.g., !@#$%^&*).

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password is secure, False otherwise.

        Raises:
            ValueError: If the password does not meet the security requirements.
        """
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

        return True

    def __init__(self, name: str, email: str, password: str, cpf: str, birthday: datetime)->None:
        self.__name = name
        if not self.__is_valid_email(email):
            raise ValueError(f"Invalid Email: {email}")
        self.__email = email
        if not self.__is_cpf_valid(cpf):
            raise ValueError(f"Invalid CPF: {cpf}")
        self.cpf = cpf
        if not self.__is_password_secure(password):