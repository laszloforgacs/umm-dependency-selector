from typing import Generic, TypeVar

from github.Repository import Repository

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

    def get_children_by_aspect(self, aspect: str) -> list[MeasurableConcept[T]]:
        return [
            child for child in self.children.values() if child.relevant_oss_aspect.name == aspect
        ]

    async def measure(self, repository: Repository) -> list[T]:
        return [
            await child.measure(repository) for child in self.children.values()
        ]

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "measurable_concepts": [child.serialize() for child in self.children.values()]
        }