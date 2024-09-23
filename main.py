# Main entry point 
from app.src.infrastructure.entrypoints.app import App

try:
    app = App()
except Exception as e:
    print(e)
