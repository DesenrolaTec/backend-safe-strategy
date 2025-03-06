from abc import ABC, abstractmethod


class ActivationsControllerInterface(ABC):
    @abstractmethod
    def read_activations(self):
        raise NotImplementedError