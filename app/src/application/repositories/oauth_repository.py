from authlib.oauth2.rfc6749 import grants
from app.src.domain.classes.user import User
from app.src.infra.models.user_model import UserModel
from app.src.infra.adapters.sql_alchemy_adapter import db
from app.src.infra.models.token_model import OAuth2Token, OAuth2TokenMixin
from app.src.infra.models.client_model import OAuth2Client, OAuth2ClientMixin
from app.src.infra.models.authcode_model import OAuth2AuthorizationCode, OAuth2AuthorizationCodeMixin
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)

query_client = create_query_client_func(db.session, OAuth2Client)
save_token = create_save_token_func(db.session, OAuth2Token)
authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)
require_oauth = ResourceProtector()

def config_oauth(app):

    authorization.init_app(app)
    # support all grants
    authorization.register_grant(PasswordGrant)
    authorization.register_grant(RefreshTokenGrant)

    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())

# Classe desacoplada para gerenciamento do grant de senha
class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, email, password):
        user = UserModel.query.filter_by(email=email).first()
        if user and user.password == password:
            return user


# Classe desacoplada para gerenciamento do refresh token
class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        token = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if token and token.is_refresh_token_active():
            return token

    def authenticate_user(self, credential):
        return UserModel.query.get(credential.user_id)

    def revoke_old_credential(self, credential):
        credential.revoked = True
        db.session.add(credential)
        db.session.commit()

class OauthRepository(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none',
    ]

    def __init__(self) -> None:
        self.__session = db.session

    def save_authorization_code(self, code, request):
        code_challenge = request.data.get('code_challenge')
        code_challenge_method = request.data.get('code_challenge_method')
        auth_code = OAuth2AuthorizationCode(
            code=code,
            client_id=request.client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=request.user.id,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
        )
        try:
            self.__session.add(auth_code)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise Exception(f"Erro ao salvar o código de autorização: {str(e)}")
        return auth_code

    def query_authorization_code(self, code, client):
        auth_code = OAuth2AuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if auth_code and not auth_code.is_expired():
            return auth_code
        return None

    def delete_authorization_code(self, authorization_code):
        try:
            self.__session.delete(authorization_code)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise Exception(f"Erro ao deletar o código de autorização: {str(e)}")

    def authenticate_user_authorization_code(self, authorization_code):
        return UserModel.query.get(authorization_code.user_id)