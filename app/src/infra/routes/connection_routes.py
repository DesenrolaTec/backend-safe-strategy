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
            "user_groups": []
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
            return jsonify({'error': 'Erro ao criar conexão.'}), 500.

    def register_routes(self, app: Flask) -> None:
        @app.route('/connections', methods=['POST'])
        @require_oauth('profile')
        def create_connection():
            return self._create_connection()