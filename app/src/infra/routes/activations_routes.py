import json
from authlib.integrations.flask_oauth2 import current_token
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from app.src.application.repositories.oauth_repository import require_oauth
from app.src.domain.interfaces.activations_controller_interface import ActivationsControllerInterface


class ActivationsRoutes:
    def __init__(self,
                 app: Flask,
                 conn_controller: ActivationsControllerInterface) -> None:
        self._controller = conn_controller
        self.register_routes(app)

    def _read_activations(self):
        try:
            response = self._controller.read_activations()
            if not response:
                return jsonify([]), 200
            return jsonify(response), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar conexão: {str(e)}'}), 500


    def _create_activations(self):
        try:
            data = request.get_json()
            response = self._controller.create_activations(data)
            if not response:
                return jsonify(""), 404
            return jsonify("Ativação feita com sucesso!"), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar conexão: {str(e)}'}), 500

    def _update_activations(self, activation_id: int):
        try:
            data = request.get_json()
            response = self._controller.update_activations(data, activation_id)
            if not response:
                return jsonify([]), 404
            return jsonify("Ativação atualizada com sucesso!"), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar conexão: {str(e)}'}), 500

    def _delete_activations(self, activation_id: int):
        try:
            response = self._controller.delete_activations(activation_id)
            if not response:
                return jsonify([]), 404
            return jsonify("Ativação deletada com sucesso!"), 200
        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': f'Erro ao criar conexão: {str(e)}'}), 500

    def register_routes(self, app: Flask) -> None:
        @app.route('/activations', methods=['GET'])
        @require_oauth('profile')
        def read_activations():
            return self._read_activations()

        @app.route('/activations', methods=['POST'])
        @require_oauth('profile')
        def create_activations():
            return self._create_activations()

        @app.route('/activations/<int:activation_id>', methods=['PATCH'])
        @require_oauth('profile')
        def update_activations(activation_id):
            return self._update_activations(activation_id)

        @app.route('/activations/<int:activation_id>', methods=['DELETE'])
        @require_oauth('profile')
        def delete_activations(activation_id):
            return self._delete_activations(activation_id)