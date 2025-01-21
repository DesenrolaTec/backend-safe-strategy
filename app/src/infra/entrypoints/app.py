from flask import Flask
from app.src.application.config.config import Config
from app.src.infra.routes.user_routes import UserRoutes
from app.src.infra.routes.oauth_routes import OauthRoutes
from app.src.infra.routes.connection_routes import ConnectionRoutes
from app.src.infra.adapters.sql_alchemy_adapter import db
from app.src.application.repositories.oauth_repository import config_oauth
from app.src.infra.entrypoints.bootstrap.bootstrap import Bootstrap

class App:
    def __init__(self, environment: str = "prod"):
        self.__config = Config(environment)
        self.__bootstrap = Bootstrap()
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
        UserRoutes(app=self.app, user_controller=self.__bootstrap.user_controller)
        ConnectionRoutes(app=self.app, conn_controller=self.__bootstrap.connection_controller)
    
    def run(self):
        app = self.app
        context = ('app/certs/server.key', 'app/certs/server.crt')
        app.run(host=self.__config.get("APP_HOST"), 
                port=self.__config.get("APP_PORT"), 
                debug=self.__config.get("FLASK_DEBUG_MODE"),
                ssl_context=context)
        return app
    
# ssl_context=context