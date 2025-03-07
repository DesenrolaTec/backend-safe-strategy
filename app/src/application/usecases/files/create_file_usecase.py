

from dataclasses import dataclass
import os
import uuid
from app.src.domain.interfaces.files_adapter_interface import FilesAdapterInterface
from app.src.domain.interfaces.usecase_interface import UseCaseInterface

@dataclass
class OutputDto:
    file_url: str

class CreateFileUsecase(UseCaseInterface):
        
        
    def execute(self, file_adapter: FilesAdapterInterface) -> OutputDto:
        
        if file_adapter.get_extension() not in ['.txt', '.stg']:
            raise Exception('Invalid file extension')
        
        abs_base_path = '/var/www/backend/static/'
        
        
        
        sub_path = 'uploads/'
        
        new_file_name = f'{uuid.uuid4().hex}{file_adapter.get_extension()}'
        new_base_path = f'{abs_base_path}{sub_path}'
        abs_base_path_file = f'{new_base_path}{new_file_name}'
        
        os.makedirs(new_base_path, exist_ok=True)
        
        file_adapter.save(path=abs_base_path_file)        
        
        file_url = f'/{sub_path}{new_file_name}'
        
        return OutputDto(file_url=file_url)