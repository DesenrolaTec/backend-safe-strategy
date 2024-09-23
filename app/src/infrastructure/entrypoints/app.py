from flask import Flask
from app.src.application.routes.user_routes import setup_user_routes


class App:

    def __init__(self, config=None):
        app = Flask(__name__)
        app.config.update(config)
        self.app = app

    def __setup_app(self):

        app = self.app
        setup_user_routes(app)
        return app

    def run(self):

        app = self.__setup_app()
        app.run(host='0.0.0.0', port=3000, debug=True)

        return app