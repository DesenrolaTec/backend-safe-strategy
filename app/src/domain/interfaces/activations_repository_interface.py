from abc import ABC, abstractmethod


class ActivationsRepositoryInterface(ABC):
    @abstractmethod
    def read_id(self, activation_id: int):
        raise NotImplementedError

    @abstractmethod
    def read_all(self):
        raise NotImplementedError

    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def update(self, data, activation_id):
        raise NotImplementedError

    @abstractmethod
    def delete(self, activation_id: int):
        raise NotImplementedError