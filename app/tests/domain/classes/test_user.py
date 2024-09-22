import pytest
from datetime import datetime
from app.src.domain.classes.user import Validator, User
from app.src.application.exceptions.user_exceptions import (InvalidBirthdayError,
                                                        InvalidCPFError,
                                                        InvalidEmailError,
                                                        WeakPasswordError)

def test_ensure_valid_email_success():
    # Arrange
    email = "teste@gmail.com"
    validator = Validator()

    # Act
    response = validator.ensure_valid_email(email=email)

    # Assert
    assert response == email

def test_ensure_valid_email_error_email_long():
    # Arrange
    email = ""
    for i in range(0, 255):
        email = f"{email}k"
    email = f"{email}@gmail.com"
    validator = Validator()

    # Act/Assert
    with pytest.raises(InvalidEmailError, match="Email is too long"):
        validator.ensure_valid_email(email=email)

def test_ensure_valid_email_error_pattern():
    # Arrange
    email = "emailcom"
    validator = Validator()

    # Act/Assert
    with pytest.raises(InvalidEmailError, match="Email is not valid"):
        validator.ensure_valid_email(email=email)

def test_ensure_valid_cpf_success():
    # Arrange
    cpf = "663.953.500-99"
    validator = Validator()

    # Act
    response = validator.ensure_valid_cpf(cpf=cpf)
    
    # Assert
    assert response == "66395350099"

def test_ensure_valid_cpf_error_length():
    # Arrange
    cpf = "663.953.500-999"
    validator = Validator()

    # Act/Assert]
    with pytest.raises(InvalidCPFError, match="Invalid CPF"):
        validator.ensure_valid_cpf(cpf=cpf)

def test_ensure_valid_cpf_error_digits():
    # Arrange
    cpf = "663.953.500-99a"
    validator = Validator()

    # Act/Assert]
    with pytest.raises(InvalidCPFError, match="Invalid CPF"):
        validator.ensure_valid_cpf(cpf=cpf)

def test_ensure_password_secure_success():
    # Arrange
    password = "Aa1!strong"
    validator = Validator()

    # Act
    response = validator.ensure_password_secure(password=password)

    # Assert
    assert response == password

def test_ensure_password_secure_error_length():
    # Arrange
    password = "Aa1"
    validator = Validator()

    # Act/Assert
    with pytest.raises(WeakPasswordError, match="Password must be at least 8 characters long."):
        validator.ensure_password_secure(password=password)

def test_ensure_password_secure_error_regex_uppercase():
    # Arrange
    password = "aabbccdd"
    validator = Validator()

    # Act/Assert
    with pytest.raises(WeakPasswordError, match="Password must contain at least one uppercase letter."):
        validator.ensure_password_secure(password=password)

def test_ensure_password_secure_error_regex_lowercase():
    # Arrange
    password = "AABBCCDD"
    validator = Validator()

    # Act/Assert
    with pytest.raises(WeakPasswordError, match="Password must contain at least one lowercase letter."):
        validator.ensure_password_secure(password=password)

def test_ensure_password_secure_error_regex_onedigit():
    # Arrange
    password = "AABBCCdd"
    validator = Validator()

    # Act/Assert
    with pytest.raises(WeakPasswordError, match="Password must contain at least one digit."):
        validator.ensure_password_secure(password=password)

def test_ensure_password_secure_error_regex_one_special_caractere():
    # Arrange
    password = "AABBC1dd"
    validator = Validator()

    # Act/Assert
    with pytest.raises(WeakPasswordError, match="Password must contain at least one special character."):
        validator.ensure_password_secure(password=password)

def test_ensure_valid_birthday_success():
    # Arrange
    birthday = "2000-12-27"
    validator = Validator()

    # Act
    response = validator.ensure_valid_birthday(birthday=birthday)

    # Assert
    assert response == "2000-12-27"

def test_ensure_valid_birthday_error_format():
    # Arrange
    birthday = "27/12/2000"
    validator = Validator()

    # Act/Assert
    with pytest.raises(InvalidBirthdayError, match="Birthday format must be YYYY-MM-DD"):
        validator.ensure_valid_birthday(birthday=birthday)


def test_ensure_valid_birthday_error_age():
    # Arrange
    today = datetime.today()
    birthday = today.strftime('%Y-%m-%d')
    validator = Validator()

    # Act/Assert
    with pytest.raises(InvalidBirthdayError, match="Person must be at least 18 years old."):
        validator.ensure_valid_birthday(birthday=birthday)


def test_user_success():
    # Arrange
    name = "Usuario Teste"
    email = "email@email.com"
    password = "Aa1!strong"
    cpf = "663.953.500-99"
    birthday = "2000-12-27"

    # Act
    response = User(name=name,
                    email=email,
                    password=password,
                    cpf=cpf,
                    birthday=birthday)
    
    # Assert
    assert isinstance(response, User)

def test_gets_user():
    # Arrange
    name = "Usuario Teste"
    email = "email@email.com"
    password = "Aa1!strong"
    cpf = "663.953.500-99"
    birthday = "2000-12-27"
    user = User(name=name,
                    email=email,
                    password=password,
                    cpf=cpf,
                    birthday=birthday)

    # Act
    response_name = user.name
    response_email = user.email
    response_password = user.password
    response_cpf = user.cpf
    response_birthday = user.birthday

    # Assert
    assert response_name == name
    assert response_email == email
    assert response_password == password
    assert response_cpf == "66395350099"
    assert response_birthday == birthday

def test_sets_user():
    # Arrange
    name = "Usuario Teste"
    email = "email@email.com"
    password = "Aa1!strong"
    cpf = "305.150.299-55"
    birthday = "2000-12-27"
    user = User(name=name,
                    email=email,
                    password=password,
                    cpf=cpf,
                    birthday=birthday)

    # Act
    user.name = "New Usuario Teste"
    user.email = "newemail@email.com"
    user.password = "newAa1!strong"

    # Assert
    assert user.name == "New Usuario Teste"
    assert user.email == "newemail@email.com"
    assert user.password == "newAa1!strong"