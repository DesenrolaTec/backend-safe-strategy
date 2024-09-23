# Main entry point 
import os

from app.src.infrastructure.entrypoints.app import App


try:
    app = App(config={
            'SECRET_KEY': 'secret',
            'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_DATABASE_URI': 'mariadb+pymysql://root:Desenrola24*@137.184.221.197/safe_strategy',
            'OAUTHLIB_INSECURE_TRANSPORT': True,
        })

    if __name__ == '__main__':
        app.run()
except Exception as e:
    print(e)
