from abc import ABCMeta, abstractmethod

from domain.model.MeasureableConcept import MeasurableConcept
from domain.model.Result import Result
from domain.model.components.Component import CompositeComponent


class SubCharacteristic(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, MeasurableConcept]):
        self._name = name
        self._children = children
        self._weight = 0

    @property
    def weight(self) -> float:
        return self._weight

    @abstractmethod
    def run(self) -> Result:
        pass