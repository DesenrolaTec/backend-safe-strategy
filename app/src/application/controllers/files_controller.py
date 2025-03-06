from app.src.application.usecases.files.create_file_usecase import OutputDto
from app.src.domain.interfaces.files_adapter_interface import FilesAdapterInterface
from app.src.domain.interfaces.files_controller_interface import FilesControllerInterface
from werkzeug.utils import secure_filename

from app.src.domain.interfaces.usecase_interface import UseCaseInterface


class FilesController(FilesControllerInterface):

    def __init__(self, create_file_usecase: UseCaseInterface) -> None:
        self.__create_file_usecase = create_file_usecase
    
    def create_file(self, file: FilesAdapterInterface) -> OutputDto:
        return self.__create_file_usecase.execute(file)
