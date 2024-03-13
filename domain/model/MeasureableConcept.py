from abc import abstractmethod
from enum import Enum
from typing import Generic, TypeVar

from domain.model.ABCGenericMeta import ABCGenericMeta
from domain.model.Component import CompositeComponent
from domain.model.Measure import Measure

T = TypeVar('T')


class Impact(Enum):
    POSITIVE = 1
    NEGATIVE = 2


class OSSAspect(Enum):
    COMMUNITY = 1
    CODE = 2


class MeasurableConcept(CompositeComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, children: dict[str, Measure], impact: Impact, entity: str, information_need: str,
                 quality_requirement: str, relevant_oss_aspect: OSSAspect = OSSAspect.CODE, normalize_visitor=None,
                 aggregate_visitor=None):
        self._name = name
        for child in children.values():
            child.parent = self
        self._children = children
        self._impact = impact
        self._entity = entity
        self._relevant_oss_aspect = relevant_oss_aspect
        self._information_need = information_need
        self._quality_requirement = quality_requirement
        self.normalize_visitor = normalize_visitor
        self.aggregate_visitor = aggregate_visitor

    @property
    def impact(self) -> Impact:
        return self._impact

    @property
    def entity(self) -> str:
        return self._entity

    @property
    def relevant_oss_aspect(self) -> OSSAspect:
        return self._relevant_oss_aspect

    @property
    def information_need(self) -> str:
        return self._information_need

    @property
    def quality_requirement(self) -> str:
        return self._quality_requirement

    async def measure(self, repository: str) -> T:
        measurements = [
            await child.measure(repository) for child in self.children.values()
        ]
        normalized = self.normalize(measurements)
        aggregated = self.aggregate(normalized)
        return aggregated

    def normalize(self, measurements: list[T]) -> list[T]:
        return self.normalize_visitor.normalize(measurements)

    def aggregate(self, normalized_measures: list[T]) -> T:
        return self.aggregate_visitor.aggregate(normalized_measures)

    def accept_visitors(self, normalize_visitor: 'NormalizeVisitor', aggregate_visitor: 'AggregateVisitor'):
        self.normalize_visitor = normalize_visitor
        self.aggregate_visitor = aggregate_visitor
