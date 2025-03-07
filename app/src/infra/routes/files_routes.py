import json
from app.src.domain.interfaces.files_controller_interface import FilesControllerInterface
from app.src.application.repositories.oauth_repository import require_oauth
from flask import Flask, request, jsonify
from werkzeug.datastructures import FileStorage

from app.src.infra.adapters.files_adapter import FilesAdapter

class FilesRoutes:
    
    def __init__(self, app: Flask, files_controller: FilesControllerInterface) -> None:
        self._controller = files_controller
        self.register_routes(app)
        
    def __create_file(self):      
                
        if 'file' not in request.files:
                return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        
        files_adapter = FilesAdapter(file=file)        
        output_dto = self._controller.create_file(file=files_adapter)
        return jsonify({'file_url': output_dto.file_url}), 200
        
        
    def register_routes(self, app: Flask) -> None:
        
        @app.route('/api/files', methods=['POST'])
        @require_oauth('profile')
        def create_file():            
            return self.__create_file()