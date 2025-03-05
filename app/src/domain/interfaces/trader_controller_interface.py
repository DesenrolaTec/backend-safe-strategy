from abc import ABC, abstractmethod


class TraderControllerInterface(ABC):
    @abstractmethod
    def get_user_activations(self, user_cpf):
        raise NotImplementedError