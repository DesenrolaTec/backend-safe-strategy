from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from app.src.infrastructure.adapters.sql_alchemy_adapter import db
from app.src.domain.dtos.profile_dto import ProfileDto
from app.src.application.repositories.user_repository import UserRepository
from app.src.application.usecases.create_user_usecase import CreateUserUsecase, InputDto
from app.src.application.usecases.create_connection_usecase import CreateConnectionUsecase
from app.src.application.repositories.profiles_repository import ProfilesRepository
from app.src.application.repositories.oauth_repository import require_oauth

class OrganizationRoutes:
    def __init__(self, app: Flask) -> None:
        self.__repository = ProfilesRepository(db.session)
        self.__user_repository = UserRepository(db.session)
        self.__create_user_usecase = CreateUserUsecase(self.__user_repository)
        self.__usecase = CreateConnectionUsecase(databaseRepository=self.__repository)
        self.register_routes(app)

    def __create_connection(self):
        try:
            data = request.get_json()
            email = data.get("email")

            if not data or 'email' not in data:
                raise BadRequest('Dados inválidos.')

            user = self.__user_repository.get_by_email(email)

            if not user:
                input_dto = InputDto(
                    email=email
                )
                output_dto = self.__create_user_usecase.execute(input_dto=input_dto)
                user_id = self.__user_repository.get_by_email(email)
            profile_dto = ProfileDto(user_id=user_id)
            
        except:
            pass

    def register_routes(self, app: Flask) -> None:
        @app.route('/connections', methods=['POST'])
        @require_oauth('profile')
        def create_connection():
            return self.__create_connection()
        
        @app.route('/connections', methods=['GET'])
        @require_oauth('profile')
        def xpto():
            return self.__revoke_token()

        @app.route('/connections', methods=['PUT'])
        @require_oauth('profile')
        def xpto():
            return self.__revoke_token()