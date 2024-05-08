import itertools
from typing import Generic, TypeVar

from github.Repository import Repository

from domain.model.ABCGenericMeta import ABCGenericMeta
from domain.model.MeasureableConcept import OSSAspect
from domain.model.SubCharacteristic import SubCharacteristic
from domain.model.Component import CompositeComponent
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix

T = TypeVar('T')


class Characteristic(CompositeComponent, Generic[T], metaclass=ABCGenericMeta):
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
        elif len(children) == 1:
            sub_characteristic = list(children.values())[0]
            self._preference_matrix = {
                (sub_characteristic.name, sub_characteristic.name): 1
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

    async def measure(self, repository: Repository) -> list[T]:
        return [
            await child.measure(repository) for child in self.children.values()
        ]

    def serialize(self) -> dict:
        return {
            "class_name": self.__class__.__name__,
            "name": self.name,
            "sub_characteristics": [child.serialize() for child in self.children.values()]
        }
