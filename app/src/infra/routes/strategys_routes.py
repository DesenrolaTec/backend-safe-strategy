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
            return jsonify({'error': f'Erro ao criar estrategia: {e}'}), 500

    def _read_strategies(self) -> jsonify:
        try:
            response = self._controller.read_strategies()
            return jsonify(response), 201
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao ler estrategias: {e}'}), 500

    def _delete_strategies(self, id):
        try:
            self._controller.delete_strategies(id = id)
            return jsonify("Estrategia deletada com sucesso!"), 201
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao ler estrategias: {e}'}), 500

    def register_routes(self, app: Flask) -> None:
        @app.route('/strategies', methods=['POST'])
        @require_oauth('profile')
        def create_strategies():
            return self._create_strategies()

        @app.route('/strategies', methods=['GET'])
        @require_oauth('profile')
        def read_strategies():
            return self._read_strategies()

        @app.route('/strategies/<id>', methods=['DELETE'])
        @require_oauth('profile')
        def delete_strategies(id: int):
            return self._delete_strategies(id = id)