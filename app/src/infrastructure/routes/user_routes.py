from flask import jsonify, request
from app.src.infrastructure.adapters.sql_alchemy_adapter import db
from werkzeug.exceptions import BadRequest
from app.src.application.repositories.user_repository import UserRepository
from app.src.application.usecases.create_user_usecase import CreateUserUsecase, InputDto

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

class UserRoutes:
    def __init__(self, app: Flask) -> None:
        self.__repository = UserRepository(db.session)
        self.__create_user_usecase = CreateUserUsecase(self.__repository)

        # Registra as rotas no aplicativo Flask
        self.register_routes(app)

    def __create_user(self) -> jsonify:
        try:
            # Obter dados do JSON enviado pelo cliente
            data = request.get_json()

            # Validação básica
            if not data or 'name' not in data or 'email' not in data or 'password' not in data:
                raise BadRequest('Dados inválidos.')

            input_dto = InputDto(
                name=data.get("name"),
                email=data.get("email"),
                password=data.get("password"),
                cpf=data.get("cpf"),
                birthday=data.get("birthday")
            )
            
            output_dto = self.__create_user_usecase.execute(input_dto=input_dto)

            return jsonify(output_dto), 201  # 201 Created

        except BadRequest as e:
            return jsonify({'error': str(e)}), 400  # 400 Bad Request
        except Exception as e:
            return jsonify({'error': 'Erro ao criar usuário.'}), 500  # 500 Internal Server Error
    
    def __get_user_by_cpf(self, ):
        data = request.json
        user_cpf = data.get('cpf').replace(".", "").replace("-", "")

        if user_cpf is None:
            return jsonify({'error': 'User CPF is required'}), 400

        user = self.__repository.get_by_id(user_cpf)
        if user:
            return jsonify(user.to_dict()), 200  # Supondo que você tenha um método to_dict
        return jsonify({'error': 'User not found'}), 404
        
    def register_routes(self, app: Flask) -> None:
        @app.route('/api/users', methods=['POST'])
        def create_user():
            return self.__create_user()
        
        @app.route('/api/users/get', methods=['GET'])
        def get_user():
            return self.__get_user_by_cpf()        