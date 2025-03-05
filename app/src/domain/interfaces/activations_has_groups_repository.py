from abc import ABC, abstractmethod

class ActivationsHasGroupsRepository(ABC):
    @abstractmethod
    def read_activations_by_group(self, groups_id: int) -> list:
        raise NotImplementedError