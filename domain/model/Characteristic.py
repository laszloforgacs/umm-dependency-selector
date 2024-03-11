import itertools
import math
from abc import abstractmethod, ABCMeta

from domain.model.MeasureableConcept import OSSAspect
from domain.model.Result import Result
from domain.model.SubCharacteristic import SubCharacteristic
from domain.model.components.Component import CompositeComponent
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class Characteristic(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, SubCharacteristic],
                 preference_matrix: PrefMatrix = {}):
        self._name = name
        for child in children.values():
            child.parent = self
        self._children = children
        if len(preference_matrix) == 0 and len(children) > 1:
            sub_characteristic_names = list(children.keys())
            preferences = list(itertools.combinations(sub_characteristic_names, 2))
            self._preference_matrix = {
                (sub_characteristic1, sub_characteristic2): None
                for sub_characteristic1, sub_characteristic2 in preferences
            }
        else:
            self._preference_matrix = preference_matrix
        self._weight = 0
        self._all_possible_aspects: list[str] = [aspect.name for aspect in OSSAspect]

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def preference_matrix(self) -> PrefMatrix:
        return self._preference_matrix

    @preference_matrix.setter
    def preference_matrix(self, preference_matrix: PrefMatrix):
        self._preference_matrix = preference_matrix

    def relevant_oss_aspects(self) -> set[str]:
        aspects_found = set()
        for child in self.children.values():
            aspects_found.update(child.relevant_oss_aspects())

            if aspects_found.issuperset(self._all_possible_aspects):
                return aspects_found
        return aspects_found

    @property
    def is_valid_preference_matrix(self) -> bool:
        combinations = list(itertools.combinations(self.children, 2))

        for combination in combinations:
            if combination not in self.preference_matrix or self.preference_matrix[combination] is None:
                return False

        return True

    @abstractmethod
    def run(self) -> Result:
        pass
