import itertools
from abc import abstractmethod, ABCMeta

from domain.model.Characteristic import Characteristic
from domain.model.Result import Result
from domain.model.components.Component import CompositeComponent


class Viewpoint(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, Characteristic] = {},
                 preference_matrix: dict[tuple[str, str], float | None] = {}):
        self._name = name
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
        self._preference_matrix = {}

    @property
    def preference_matrix(self) -> dict[tuple[str, str], float]:
        return self._preference_matrix

    def set_preference(self, characteristic_tuple: tuple[str, str], preference: float):
        pass

    @property
    def is_valid_preference_matrix(self) -> bool:
        return len(self.preference_matrix) > 0 and all(
            value is not None
            for value in self.preference_matrix.values()
        )

    @abstractmethod
    def run(self) -> Result:
        pass
