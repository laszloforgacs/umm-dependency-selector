import itertools
from abc import ABCMeta

from domain.model.MeasureableConcept import OSSAspect
from domain.model.Component import CompositeComponent
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class Viewpoint(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, 'Characteristic'] = {},
                 preference_matrix: PrefMatrix = {}, oss_aspect_preference_matrix: PrefMatrix = {}):
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
        if len(oss_aspect_preference_matrix) == 0:
            oss_aspect_tuples = list(itertools.combinations([aspect.name for aspect in OSSAspect], 2))
            self._oss_aspect_preference_matrix = {
                (aspect1, aspect2): None
                for aspect1, aspect2 in oss_aspect_tuples
            }
        else:
            self._oss_aspect_preference_matrix = oss_aspect_preference_matrix
        self._weight = 0

    def add_component(self, component: 'Characteristic'):
        self._children[component.name] = component

    @property
    def preference_matrix(self) -> PrefMatrix:
        return self._preference_matrix

    @property
    def oss_aspect_preference_matrix(self) -> PrefMatrix:
        return self._oss_aspect_preference_matrix

    @preference_matrix.setter
    def preference_matrix(self, preference_matrix: PrefMatrix):
        self._preference_matrix = preference_matrix

    @oss_aspect_preference_matrix.setter
    def oss_aspect_preference_matrix(self, oss_aspect_preference_matrix: PrefMatrix):
        self._oss_aspect_preference_matrix = oss_aspect_preference_matrix

    def set_preference(self, characteristic_tuple: tuple[str, str], preference: float):
        pass

    @property
    def is_valid_preference_matrix(self) -> bool:
        combinations = list(itertools.combinations(self.children, 2))

        for combination in combinations:
            if combination not in self.preference_matrix or self.preference_matrix[combination] is None:
                return False

        for aspect_combination in itertools.combinations([aspect.name for aspect in OSSAspect], 2):
            if aspect_combination not in self.oss_aspect_preference_matrix or self.oss_aspect_preference_matrix[
                aspect_combination] is None:
                return False

        for child in self.children.values():
            if not child.is_valid_preference_matrix:
                return False

        return True

    def serialize(self) -> dict:
        return {
            "class_name": self.__class__.__name__,
            "name": self.name,
            "characteristics": [child.serialize() for child in self.children.values()]
        }