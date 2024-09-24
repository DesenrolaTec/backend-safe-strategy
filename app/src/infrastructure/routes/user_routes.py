from flask import jsonify, request
from werkzeug.exceptions import BadRequest
from app.src.infrastructure.adapters.sql_alchemy_adapter import db
from app.src.application.repositories.oauth_repository import require_oauth
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
    
    def __get_user_by_cpf(self, cpf: str):
        user_cpf = cpf.replace("-", "")

        if user_cpf is None:
            return jsonify({'error': 'User CPF is required'}), 400

        user = self.__repository.get_by_id(user_cpf)
        if user:
            return jsonify(user.to_dict()), 200  # Supondo que você tenha um método to_dict
        return jsonify({'error': 'User not found'}), 404
    
    def __delete_user(self, cpf: str):
        try:
            result = self.__repository.delete(user_cpf = cpf.replace("-", ""))
            
            if result:  # Se a deleção foi bem-sucedida
                return jsonify({'message': 'User deleted successfully.'}), 204  # 204 No Content
            else:
                return jsonify({'error': 'User not found.'}), 404  # 404 Not Found

        except Exception as e:
            return jsonify({'error': 'Error deleting user.'}), 500  # 500 Internal Server Error
        
    def __update_user(self, cpf: str):
        try:
            # Obter dados do JSON enviado pelo cliente
            data = request.get_json()

            # Validação básica (dependendo dos campos que você precisa atualizar)
            if not data:
                raise BadRequest('Nenhum dado fornecido para atualização.')

            # Chamar o repositório para atualizar o usuário
            result = self.__repository.update(cpf, data)
            
            if result:
                return jsonify({'message': 'Usuário atualizado com sucesso.'}), 200  # 200 OK
            else:
                return jsonify({'error': 'Usuário não encontrado.'}), 404  # 404 Not Found

        except BadRequest as e:
            return jsonify({'error': str(e)}), 400  # 400 Bad Request
        except Exception as e:
            return jsonify({'error': 'Erro ao atualizar usuário.'}), 500  # 500 Internal Server Error
        
    def register_routes(self, app: Flask) -> None:
        @app.route('/api/users', methods=['POST'])
        @require_oauth('profile')
        def create_user():
            return self.__create_user()
        
        @app.route('/api/users/<string:user_cpf>', methods=['GET'])
        @require_oauth('profile')
        def get_user(user_cpf):
            return self.__get_user_by_cpf(cpf=user_cpf)   

        @app.route('/api/users/<string:user_cpf>', methods=['DELETE'])
        @require_oauth('profile')
        def delete_user(user_cpf):
            return self.__delete_user(cpf=user_cpf)
        
        @app.route('/api/users/<int:user_cpf>', methods=['PATCH'])
        @require_oauth('profile')
        def update_user(user_cpf):
            return self.__update_user(cpf=user_cpf)