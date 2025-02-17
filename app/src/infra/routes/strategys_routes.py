from authlib.integrations.flask_oauth2 import current_token
from app.src.application.repositories.oauth_repository import require_oauth
from app.src.domain.interfaces.strategies_controller_interface import StrategiesControllerInterface
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest


class StrategiesRoutes:
    def __init__(self, app: Flask, strategies_controller: StrategiesControllerInterface) -> None:
        self._controller = strategies_controller
        self.register_routes(app)

    def _create_strategies(self) -> jsonify:
        try:
            data = request.get_json()
            response = self._controller.create_strategies(data)
            return jsonify(response), 201
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar usuário: {e}'}), 500

    def register_routes(self, app: Flask) -> None:
        @app.route('/strategies', methods=['POST'])
        @require_oauth('profile')
        def create_strategies():
            return self._create_strategies()