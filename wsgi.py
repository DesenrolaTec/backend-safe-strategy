from app.src.infrastructure.entrypoints.app import App

try:
    app = App()
    app.run()
except Exception as e:
    print(e)