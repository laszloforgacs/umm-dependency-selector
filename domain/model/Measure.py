from abc import abstractmethod
from enum import Enum
from typing import Generic, TypeVar

from github.Repository import Repository

from domain.model.ABCGenericMeta import ABCGenericMeta
from domain.model.Component import LeafComponent, CompositeComponent
from domain.model.QualityModel import QualityModel
from domain.model.Viewpoint import Viewpoint

T = TypeVar('T')
U = TypeVar('U')


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

    @property
    @abstractmethod
    def value(self) -> T:
        pass

    @abstractmethod
    def measure(self, repository: Repository) -> T:
        pass

    def get_viewpoint(self):
        next_parent = self.parent
        while next_parent:
            if isinstance(next_parent, Viewpoint):
                return next_parent
            next_parent = next_parent.parent

        return None

    def get_quality_model(self):
        next_parent = self.parent
        while next_parent:
            if isinstance(next_parent, QualityModel):
                return next_parent
            next_parent = next_parent.parent

        return None

class BaseMeasure(Measure, LeafComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, unit: str, scale: float,
                 measurement_method: MeasurementMethod = MeasurementMethod.AUTOMATIC, visitor=None):
        self._name = name
        self._unit = unit
        self._scale = scale
        self._measurement_method = measurement_method
        self.visitor = visitor
        self._value = None

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

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T):
        self._value = value

    async def measure(self, repository: str) -> T:
        print(f"{repository.full_name}: Measuring {self.name}")
        result = await self.visitor.measure(self, repository)
        self.value = result
        return result

    def accept_visitor(self, visitor: 'BaseMeasureVisitor'):
        self.visitor = visitor

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "scale": self.scale,
            "measurement_method": self.measurement_method.name,
            "visitor": self.visitor.__class__.__name__
        }

    def pretty_print(self) -> dict:
        return {
            "name": self.name,
            "unit": self.unit,
        }


class DerivedMeasure(Measure, CompositeComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, unit: str, scale: float,
                 measurement_method: MeasurementMethod = MeasurementMethod.AUTOMATIC,
                 children: dict[str, BaseMeasure] = {}, normalize_visitor=None, aggregate_visitor=None):
        self._name = name
        self._unit = unit
        self._scale = scale
        self._measurement_method = measurement_method
        for child in children.values():
            child.parent = self
        self._children = children
        self.normalize_visitor = normalize_visitor
        self.aggregate_visitor = aggregate_visitor
        self._value = None

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

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T):
        self._value = value

    async def measure(self, repository: Repository) -> T:
        measurements = [
            (child, await child.measure(repository)) for child in self.children.values()
        ]
        normalized = self.normalize(measurements, repository)
        aggregated = self.aggregate(normalized, repository)
        print(f"{repository.full_name}: {self.name} is {aggregated}")
        self.value = aggregated
        return aggregated

    def normalize(self, measurements: list[T], repository: Repository) -> list[T]:
        return self.normalize_visitor.normalize(measurements, repository)

    def aggregate(self, normalized_measures: list[T], repository: Repository) -> U:
        return self.aggregate_visitor.aggregate(normalized_measures, repository)

    def accept_visitors(self, normalize_visitor: 'NormalizeVisitor', aggregate_visitor: 'AggregateVisitor'):
        self.normalize_visitor = normalize_visitor
        self.aggregate_visitor = aggregate_visitor

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "scale": self.scale,
            "measurement_method": self.measurement_method.name,
            "base_measures": [child.serialize() for child in self.children.values()],
            "normalize_visitor": self.normalize_visitor.__class__.__name__,
            "aggregate_visitor": self.aggregate_visitor.__class__.__name__
        }

    def pretty_print(self) -> dict:
        return {
            "name": self.name,
            "unit": self.unit,
            "base_measures": [child.pretty_print() for child in self.children.values()],
        }
