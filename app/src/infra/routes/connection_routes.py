import json
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from app.src.application.repositories.oauth_repository import require_oauth
from app.src.domain.interfaces.connection_controller_interface import ConnectionControllerInterface

class ConnectionRoutes:
    def __init__(self, app: Flask, conn_controller: ConnectionControllerInterface) -> None:
        self._controller = conn_controller
        self.register_routes(app)
        
    def _create_connection(self) -> jsonify:
        """
            {
            "user_name": "",
            "user_email": "",
            "user_cpf": "",
            "user_client_id": "",
            "user_enable": 1,
            "user_groups_ids": []
        }
        :return:
        """
        try:
            data = request.get_json()
            response = self._controller.create_connection(data)
            return jsonify(response), 201
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Erro ao criar conexão.'}), 500

    def _read_connection(self):
        try:
            response = self._controller.read_connections()
            if not response:
                return jsonify(""), 404
            return jsonify(response), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar conexão: {str(e)}'}), 500

    def _delete_connection(self,
                           conn_id: int):
        try:
            self._controller.delete_connection(conn_id = conn_id)
            return jsonify("Conexão deletada com sucesso"), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar conexão: {str(e)}'}), 500

    def register_routes(self, app: Flask) -> None:
        @app.route('/connections', methods=['POST'])
        @require_oauth('profile')
        def create_connection():
            return self._create_connection()

        @app.route('/connections', methods=['GET'])
        @require_oauth('profile')
        def read_connection():
            return self._read_connection()

        @app.route('/connections', methods=['DELETE'])
        @require_oauth('profile')
        def delete_connection(conn_id: int):
            return self._delete_connection(conn_id = conn_id)