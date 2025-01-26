from authlib.integrations.flask_oauth2 import current_token
from app.src.application.repositories.oauth_repository import require_oauth
from authlib.integrations.flask_oauth2 import current_token
from app.src.domain.interfaces.user_controller_interface import UserControllerInterface

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

class UserRoutes:
    def __init__(self, app: Flask, user_controller: UserControllerInterface) -> None:
        self._controller = user_controller
        self.register_routes(app)

    def _create_user(self) -> jsonify:
        try:
            data = request.get_json()
            response = self._controller.create_user(data)
            return jsonify(response), 201
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Erro ao criar usuário.'}), 500
    
    def _get_user_by_cpf(self, cpf: str):
        if cpf is None:
            return jsonify({'error': 'User CPF is required'}), 400
        user = self._controller.get_user(user_cpf=cpf)
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'User not found'}), 404
    
    def _delete_user(self, cpf: str):
        try:
            user = self._controller.delete_user(cpf)
            if user:
                return jsonify(user), 204
            else:
                return jsonify({'error': 'User not found.'}), 404

        except Exception as e:
            return jsonify({'error': 'Error deleting user.'}), 500
        
    def _update_user(self,):
        try:
            data = request.get_json()
            if not data:
                raise BadRequest('Nenhum dado fornecido para atualização.')
            result = self._controller.update_user(user_data=data)
            if result:
                return jsonify({'message': 'Usuário atualizado com sucesso.'}), 200
            else:
                return jsonify({'error': 'Usuário não encontrado.'}), 404
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao atualizar usuário {e}'}), 500
        
    def _update_password(self,):
        try:
            data = request.get_json()
            if not data:
                raise BadRequest('Nenhum dado fornecido para atualização.')
            user_cpf = current_token.user.cpf
            user = self._controller.get_user(user_cpf=user_cpf)
            if user.get("password") != data['old_password']:
                return jsonify({'error': 'Senha antiga incorreta.'}), 400
            result = self._controller.update_user(user_data=data)
            if result:
                return jsonify({'message': 'Usuário atualizado com sucesso.'}), 200
            else:
                return jsonify({'error': 'Usuário não encontrado.'}), 404
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao atualizar usuário {e}'}), 500
        
    def register_routes(self, app: Flask) -> None:
        @app.route('/api/users', methods=['POST'])
        @require_oauth('profile')
        def create_user():
            return self._create_user()
        
        @app.route('/api/users/me', methods=['GET'])
        @require_oauth('profile')
        def get_user():
            user = current_token.user
            user_cpf = user.cpf
            return self._get_user_by_cpf(cpf=user_cpf)   

        @app.route('/api/users/<string:user_cpf>', methods=['DELETE'])
        @require_oauth('profile')
        def delete_user(user_cpf):
            return self._delete_user(cpf=user_cpf)
        
        @app.route('/api/users', methods=['PATCH'])
        @require_oauth('profile')
        def update_user():
            return self._update_user()
        
        @app.route('/api/users/me', methods=['PATCH'])
        @require_oauth('profile')
        def update_password():
            return self._update_password()