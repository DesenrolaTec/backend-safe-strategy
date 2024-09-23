from flask import Flask
from app.src.application.config.config import Config
from app.src.infrastructure.adapters.sql_alchemy_adapter import db
from app.src.infrastructure.routes.user_routes import UserRoutes


class App:
    def __init__(self, environment:str="prod"):
        self.__config = Config()
        app = Flask(__name__)
        config = self.__setup_config()
        app.config.update(config)
        self.app = app

    def __setup_config(self, )->dict:
        return{
            'SECRET_KEY': self.__config.get("SECRET_KEY"),
            'OAUTH2_REFRESH_TOKEN_GENERATOR': self.__config.get("OAUTH2_REFRESH_TOKEN_GENERATOR"),
            'SQLALCHEMY_TRACK_MODIFICATIONS': self.__config.get("SQLALCHEMY_TRACK_MODIFICATIONS"),
            'SQLALCHEMY_DATABASE_URI': self.__config.get("SQLALCHEMY_DATABASE_URI"),
            'OAUTHLIB_INSECURE_TRANSPORT': self.__config.get("OAUTHLIB_INSECURE_TRANSPORT")
        }

    def __setup_app(self):
        app = self.app
        db.init_app(app)
        UserRoutes(app=app)
        return app

    def run(self):
        app = self.__setup_app()
        app.run(host=self.__config.get("APP_HOST"), 
                port=self.__config.get("APP_PORT"), 
                debug=self.__config.get("FLASK_DEBUG_MODE"))
        return app