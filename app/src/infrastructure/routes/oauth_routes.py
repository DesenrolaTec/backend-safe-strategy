from flask import Flask, request, jsonify
from app.src.application.repositories.oauth_repository import OauthRepository, authorization, require_oauth
from authlib.integrations.flask_oauth2 import current_token

class OauthRoutes:
    def __init__(self, app: Flask) -> None:
        self.__repository = OauthRepository()
        self.__authorization = authorization
        self.register_routes(app)

    def __issue_token(self):
        return self.__authorization.create_token_response()
    
    def __revoke_token(self):
        return self.__authorization.create_endpoint_response('revocation')

    def register_routes(self, app: Flask) -> None:
        @app.route('/oauth/token', methods=['POST'])
        def issue_token():
            return self.__issue_token()
        
        @app.route('/oauth/revoke', methods=['POST'])
        def revoke_token():
            return self.__revoke_token()
        
        @app.route('/api/me')
        @require_oauth('profile')  # Utilizando o require_oauth como atributo da classe
        def api_me():
            user = current_token.user
            return jsonify(id=user.id, email=user.email)
