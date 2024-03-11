from typing import Generic, TypeVar

from domain.model.ABCGenericMeta import ABCGenericMeta
from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect
from domain.model.Component import CompositeComponent

T = TypeVar('T')


class SubCharacteristic(CompositeComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, children: dict[str, MeasurableConcept[T]]):
        self._name = name
        for child in children.values():
            child.parent = self
        self._children = children
        self._weight = 0
        self._all_possible_aspects: list[str] = [aspect.name for aspect in OSSAspect]

    @property
    def weight(self) -> float:
        return self._weight

    def relevant_oss_aspects(self) -> set[str]:
        aspects_found = set()
        for child in self.children.values():
            aspects_found.add(child.relevant_oss_aspect.name)

            if aspects_found.issuperset(self._all_possible_aspects):
                return aspects_found
        return aspects_found

    def measure(self) -> list[T]:
        return [
            child.measure() for child in self.children.values()
        ]
