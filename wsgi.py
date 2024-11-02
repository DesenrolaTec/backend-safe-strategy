from app.src.infrastructure.entrypoints.app import App

setup = App()
app = setup.run()