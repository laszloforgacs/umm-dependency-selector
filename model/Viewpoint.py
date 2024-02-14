from abc import abstractmethod, ABCMeta

from model.Characteristic import Characteristic
from model.Result import Result
from model.components.Component import CompositeComponent


class Viewpoint(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, Characteristic], preference_matrix: dict[tuple[str, str], float]):
        self._name = name
        self._children = children
        self._preference_matrix = preference_matrix
        self._weight = 0

    @property
    def preference_matrix(self) -> dict[tuple[str, str], float]:
        return self._preference_matrix

    @abstractmethod
    def run(self) -> Result:
        pass