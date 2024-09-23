# Main entry point 
from app.src.infrastructure.entrypoints.app import App

try:
    app = App()
    if __name__ == '__main__':
        app.run()
except Exception as e:
    print(e)
