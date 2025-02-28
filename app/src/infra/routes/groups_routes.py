import json
from werkzeug.exceptions import BadRequest
from app.src.application.repositories.oauth_repository import require_oauth
from authlib.integrations.flask_oauth2 import current_token
from flask import Flask, jsonify, request
from app.src.domain.interfaces.groups_controller_interface import GroupsControllerInterface


class GroupsRoutes:
    def __init__(self, app: Flask, groups_controller: GroupsControllerInterface) -> None:
        self._controller = groups_controller
        self.register_routes(app)

    def __create_group(self,
                       user_cpf: str) -> jsonify:
        try:
            data = request.get_json()
            response = self._controller.create_group(user_cpf=user_cpf, data = data)
            return jsonify({'sucesso': response.get("message")}), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar o grupo: {e}'}), 500

    def __get_groups(self,
                     user_cpf: str):
        output_dto = self._controller.get_groups(user_cpf = user_cpf)
        if output_dto.groups:
            return jsonify({'groups': output_dto.groups}), 201
        return jsonify({'error': f'{output_dto.message}'}), 404

    def __delete_groups(self,
                        group_id: int):
        try:
            self._controller.delete_group(group_id=group_id)
            return jsonify("Grupo deletado com sucesso!"), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    def __update_group(self):
        try:
            data = request.get_json()
            self._controller.update_group(data = data)
            return jsonify({'sucesso': "Grupos atualizados com sucesso!"}), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar o grupo: {e}'}), 500

    def register_routes(self, app: Flask) -> None:
        @app.route('/groups', methods=['POST'])
        @require_oauth('profile')
        def create_group():
            user = current_token.user
            user_cpf = user.cpf
            return self.__create_group(user_cpf = user_cpf)

        @app.route('/groups', methods=['GET'])
        @require_oauth('profile')
        def get_groups():
            user = current_token.user
            user_cpf = user.cpf
            return self.__get_groups(user_cpf = user_cpf)

        @app.route('/groups/<group_id>', methods=['DELETE'])
        @require_oauth('profile')
        def delete_groups(group_id):
            return self.__delete_groups(group_id=group_id)

        @app.route('/groups', methods=['PATCH'])
        @require_oauth('profile')
        def update_group():
            return self.__update_group()