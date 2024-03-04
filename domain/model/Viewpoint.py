import itertools
import math
from abc import abstractmethod, ABCMeta

from domain.model.Characteristic import Characteristic
from domain.model.Result import Result
from domain.model.components.Component import CompositeComponent
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class Viewpoint(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, Characteristic] = {},
                 preference_matrix: PrefMatrix = {}):
        self._name = name
        for child in children.values():
            child.parent = self
        self._children = children
        if len(preference_matrix) == 0 and len(children) > 1:
            characteristic_names = list(children.keys())
            preference_tuples = list(itertools.combinations(characteristic_names, 2))
            self._preference_matrix = {
                (characteristic1, characteristic2): None
                for characteristic1, characteristic2 in preference_tuples
            }
        else:
            self._preference_matrix = preference_matrix
        self._weight = 0

    def add_component(self, component: Characteristic):
        self._children[component.name] = component

    @property
    def preference_matrix(self) -> PrefMatrix:
        return self._preference_matrix

    @preference_matrix.setter
    def preference_matrix(self, preference_matrix: PrefMatrix):
        self._preference_matrix = preference_matrix

    def set_preference(self, characteristic_tuple: tuple[str, str], preference: float):
        pass

    @property
    def is_valid_preference_matrix(self) -> bool:
        combinations = list(itertools.combinations(self.children, 2))
        combinations_count = math.comb(len(self.children), 2)
        matrix_count = len(self.preference_matrix)

        if matrix_count != combinations_count:
            return False

        for combination in combinations:
            if combination not in self.preference_matrix or self.preference_matrix[combination] is None:
                return False

        return True

    @abstractmethod
    def run(self) -> Result:
        pass
