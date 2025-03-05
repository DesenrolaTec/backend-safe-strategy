from abc import ABC, abstractmethod


class ActivationsRepositoryInterface(ABC):
    @abstractmethod
    def read_id(self, activation_id: int):
        raise NotImplementedError