from abc import ABC, abstractmethod

class ActivationsHasGroupsRepositoryInterface(ABC):
    @abstractmethod
    def read_activations_by_group(self, groups_id: int) -> list:
        raise NotImplementedError

    @abstractmethod
    def read_activations_by_id(self, id: int):
        raise NotImplementedError