import json
from app.src.application.repositories.oauth_repository import require_oauth
from authlib.integrations.flask_oauth2 import current_token
from flask import Flask, jsonify
from app.src.domain.interfaces.groups_controller_interface import GroupsControllerInterface


class GroupsRoutes:
    def __init__(self, app: Flask, groups_controller: GroupsControllerInterface) -> None:
        self._controller = groups_controller
        self.register_routes(app)

    """def __create_group(self) -> jsonify:
        try:
            pass
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar usuário: {e}'}), 500"""

    def __get_groups(self,
                     user_cpf: str):
        output_dto = self._controller.get_groups(user_cpf = user_cpf)
        if output_dto.groups:
            return jsonify({'groups': output_dto.groups}), 201
        return jsonify({'error': f'{output_dto.message}'}), 404

    def register_routes(self, app: Flask) -> None:
        """@app.route('/groups', methods=['POST'])
        @require_oauth('profile')
        def create_group():
            return self._create_user()"""

        @app.route('/groups', methods=['GET'])
        @require_oauth('profile')
        def get_groups():
            user = current_token.user
            user_cpf = user.cpf
            return self.__get_groups(user_cpf = user_cpf)