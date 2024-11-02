from typing import Final
from dataclasses import dataclass
from app.src.domain.dtos.profile_dto import ProfileDto
from app.src.domain.interfaces.profiles_repository_interface import ProfilesRepositoryInterface
from app.src.domain.interfaces.usecase_interface import UsecaseInterface

class CreateConnectionUsecase(UsecaseInterface):
    def __init__(self, databaseRepository: ProfilesRepositoryInterface):
        self.__db_repository = databaseRepository

    def execute(self, input_dto: ProfileDto)->ProfileDto:
        self.__db_repository.create(connection = input_dto)
        return input_dto

