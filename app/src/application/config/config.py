import os
from dotenv import load_dotenv

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, environment: str = "prod"):
        # Para evitar a reinicialização em novas chamadas
        if not hasattr(self, '_initialized'):
            if environment == "prod":
                load_dotenv(dotenv_path="app/infra/prod/.env")
            else:
                load_dotenv(dotenv_path="app/infra/dev/.env")
            
            self.SECRET_KEY = os.getenv('SECRET_KEY')
            self.OAUTH2_REFRESH_TOKEN_GENERATOR = True
            self.SQLALCHEMY_TRACK_MODIFICATIONS = False
            self.SQLALCHEMY_DATABASE_IP = os.getenv('SQLALCHEMY_DATABASE_IP')
            self.SQLALCHEMY_DATABASE_PASSWORD = os.getenv('SQLALCHEMY_DATABASE_PASSWORD')
            self.SQLALCHEMY_DATABASE_URI = f"mariadb+pymysql://root:{self.SQLALCHEMY_DATABASE_PASSWORD}@{self.SQLALCHEMY_DATABASE_IP}/safe_strategy"
            print(self.SQLALCHEMY_DATABASE_URI)
            self.OAUTHLIB_INSECURE_TRANSPORT = False
            self.APP_HOST = os.getenv('APP_HOST')
            self.APP_PORT = os.getenv('APP_PORT')
            self.FLASK_DEBUG_MODE = True
            self._initialized = True

    def get(self, key: str):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f"A chave '{key}' não existe nas configurações de ambiente.")