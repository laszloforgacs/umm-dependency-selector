from abc import abstractmethod
from enum import Enum
from typing import Generic, TypeVar

from github.Repository import Repository

from domain.model.ABCGenericMeta import ABCGenericMeta
from domain.model.Component import LeafComponent, CompositeComponent

T = TypeVar('T')


class MeasurementMethod(Enum):
    AUTOMATIC = 1
    MANUAL = 2


class Measure(Generic[T], metaclass=ABCGenericMeta):
    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def unit(self) -> str:
        pass

    @property
    @abstractmethod
    def scale(self) -> float:
        pass

    @property
    @abstractmethod
    def measurement_method(self) -> MeasurementMethod:
        pass

    @abstractmethod
    def measure(self, repository: str) -> T:
        pass


class BaseMeasure(Measure, LeafComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, unit: str, scale: float, measurement_method: MeasurementMethod, visitor=None):
        self._name = name
        self._unit = unit
        self._scale = scale
        self._measurement_method = measurement_method
        self.visitor = visitor

    @property
    def name(self) -> str:
        return self._name

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def scale(self) -> float:
        return self._scale

    @property
    def measurement_method(self) -> MeasurementMethod:
        return self._measurement_method

    async def measure(self, repository: str) -> T:
        return await self.visitor.measure(self, repository)

    def accept_visitor(self, visitor: 'BaseMeasureVisitor'):
        self.visitor = visitor


class DerivedMeasure(Measure, CompositeComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, unit: str, scale: float, measurement_method: MeasurementMethod,
                 children: dict[str, BaseMeasure], normalize_visitor=None, aggregate_visitor=None):
        self._name = name
        self._unit = unit
        self._scale = scale
        self._measurement_method = measurement_method
        for child in children.values():
            child.parent = self
        self._children = children
        self.normalize_visitor = normalize_visitor
        self.aggregate_visitor = aggregate_visitor

    @property
    def name(self) -> str:
        return self._name

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def scale(self) -> float:
        return self._scale

    @property
    def measurement_method(self) -> MeasurementMethod:
        return self._measurement_method

    async def measure(self, repository: Repository) -> T:
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
