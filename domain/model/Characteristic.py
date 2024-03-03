from abc import abstractmethod, ABCMeta

from domain.model.Result import Result
from domain.model.SubCharacteristic import SubCharacteristic
from domain.model.components.Component import CompositeComponent
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class Characteristic(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, SubCharacteristic], preference_matrix: PrefMatrix = {}):
        self._name = name
        self._children = children
        self._preference_matrix = preference_matrix
        self._weight = 0

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def preference_matrix(self) -> PrefMatrix:
        return self._preference_matrix

    @property
    def is_valid_preference_matrix(self) -> bool:
        return len(self.preference_matrix) > 0 and all(
            value is not None
            for value in self.preference_matrix.values()
        )

    @abstractmethod
    def run(self) -> Result:
        pass
