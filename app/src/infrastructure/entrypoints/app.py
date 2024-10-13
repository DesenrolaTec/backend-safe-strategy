from flask import Flask
from app.src.application.config.config import Config
from app.src.infrastructure.routes.user_routes import UserRoutes
from app.src.infrastructure.routes.oauth_routes import OauthRoutes
from app.src.infrastructure.adapters.sql_alchemy_adapter import db
from app.src.application.repositories.oauth_repository import config_oauth

class App:
    def __init__(self, environment: str = "prod"):
        self.__config = Config(environment)
        self.app = Flask(__name__)
        self.__setup_config()
        self.__setup_app()

    def __setup_config(self):
        self.app.config.update({
            'SECRET_KEY': self.__config.get("SECRET_KEY"),
            'OAUTH2_REFRESH_TOKEN_GENERATOR': self.__config.get("OAUTH2_REFRESH_TOKEN_GENERATOR"),
            'SQLALCHEMY_TRACK_MODIFICATIONS': self.__config.get("SQLALCHEMY_TRACK_MODIFICATIONS"),
            'SQLALCHEMY_DATABASE_URI': self.__config.get("SQLALCHEMY_DATABASE_URI"),
            'OAUTHLIB_INSECURE_TRANSPORT': self.__config.get("OAUTHLIB_INSECURE_TRANSPORT")
        })

    def __setup_app(self):
        db.init_app(self.app)
        config_oauth(self.app)
        OauthRoutes(app=self.app)
        UserRoutes(app=self.app)
    
    def run(self):
        app = self.app
        context = (
            '/etc/letsencrypt/archive/api.desenrolatec.com.br/privkey1.pem', 
            '/etc/letsencrypt/archive/api.desenrolatec.com.br/fullchain1.pem'
        )
        app.run(host=self.__config.get("APP_HOST"), 
                port=self.__config.get("APP_PORT"), 
                debug=self.__config.get("FLASK_DEBUG_MODE"),
                ssl_context=context)
        return app