from authlib.integrations.flask_oauth2 import current_token
from app.src.application.repositories.oauth_repository import require_oauth
from werkzeug.exceptions import BadRequest
from flask import Flask, jsonify

from app.src.domain.interfaces.trader_controller_interface import TraderControllerInterface


class TraderRoutes:
    def __init__(self,
                 app: Flask,
                 traders_controller: TraderControllerInterface) -> None:
        self._controller = traders_controller
        self.register_routes(app)

    def _me_activations(self, user_cpf) -> jsonify:
        try:
            response = self._controller.get_user_activations(user_cpf)
            return jsonify(response), 201
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar estrategia: {e}'}), 500

    def register_routes(self, app: Flask) -> None:
        @app.route('/traders/me/activations', methods=['GET'])
        @require_oauth('profile')
        def me_activations():
            user = current_token.user
            user_cpf = user.cpf
            return self._me_activations(user_cpf)