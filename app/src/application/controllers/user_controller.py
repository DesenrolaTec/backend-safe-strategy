from app.src.application.usecases.create_user import CreateUser, InputDto as CreateUserInputDto

class UserController:
    def __init__(self, create_user: CreateUser):
        self._create_user = create_user

    def _map_user_data(self, user_data: dict) -> CreateUserInputDto:
        return CreateUserInputDto(
            name=user_data.get('name'),
            email=user_data.get('email'),
            cpf=user_data.get('cpf'),
            password=user_data.get('password'),
            birthday=user_data.get('birthday'),
        )

    def create_user(self, user_data: dict):
        user_dto = self._map_user_data(user_data)
        output_dto = self._create_user.execute(user_dto)
        return output_dto.to_dict()