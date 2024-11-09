from app.src.application.usecases.user.create_user import CreateUserUsecase, InputDto as CreateUserInputDto
from app.src.application.usecases.user.get_user import ReadUserUsecase, InputDto as UserCpfInputDto
from app.src.application.usecases.user.delete_user import DeleteUserUsecase, InputDto as DeleteUserInputDto
from app.src.application.usecases.user.update_user import UpdateUserUsecase, InputDto as UpdateUserInputDto

class UserController:
    def __init__(self, create_user: CreateUserUsecase, get_user: ReadUserUsecase, delete_user: DeleteUserUsecase, update_user: UpdateUserUsecase) -> None:
        self._create_user = create_user
        self._get_user = get_user
        self._delete_user = delete_user
        self._update_user = update_user

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
        return output_dto.user.to_dict()
    
    def _map_user_cpf_read(self, user_cpf: str)->UserCpfInputDto:
        return UserCpfInputDto(cpf=user_cpf)

    def get_user(self, user_cpf: str):
        user_dto = self._map_user_cpf_read(user_cpf)
        output_dto = self._get_user.execute(user_dto)
        return output_dto.user.to_dict()
    
    def _map_user_cpf_delete(self, user_cpf: str)->DeleteUserInputDto:
        return DeleteUserInputDto(cpf=user_cpf)
    
    def delete_user(self, user_cpf: str):
        user_dto = self._map_user_cpf_delete(user_cpf)
        output_dto = self._delete_user.execute(user_dto)
        return output_dto.user.to_dict()
    
    def _map_user_updated_data(self, user_data: dict) -> UpdateUserInputDto:
        return UpdateUserInputDto(
            name=user_data.get('name'),
            email=user_data.get('email'),
            cpf=user_data.get('cpf'),
            password=user_data.get('password'),
            birthday=user_data.get('birthday'),
        )

    def update_user(self, user_data: dict):
        user_dto = self._map_user_updated_data(user_data)
        output_dto = self._update_user.execute(user_dto)
        return output_dto.user.to_dict()