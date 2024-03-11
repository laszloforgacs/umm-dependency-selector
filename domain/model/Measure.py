from abc import abstractmethod
from enum import Enum
from typing import Generic, TypeVar

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
    def measure(self) -> T:
        pass


class BaseMeasure(Measure, LeafComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, unit: str, scale: float, measurement_method: MeasurementMethod):
        self._name = name
        self._unit = unit
        self._scale = scale
        self._measurement_method = measurement_method

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


class DerivedMeasure(Measure, CompositeComponent, Generic[T], metaclass=ABCGenericMeta):
    def __init__(self, name: str, unit: str, scale: float, measurement_method: MeasurementMethod,
                 children: dict[str, BaseMeasure]):
        self._name = name
        self._unit = unit
        self._scale = scale
        self._measurement_method = measurement_method
        for child in children.values():
            child.parent = self
        self._children = children

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

    def measure(self) -> T:
        measurements = [
            child.measure() for child in self.children.values()
        ]
        normalized = self.normalize(measurements)
        aggregated = self.aggregate(normalized)
        return aggregated

    @abstractmethod
    def normalize(self, measurements: list[T]) -> list[T]:
        pass

    @abstractmethod
    def aggregate(self, normalized_measures: list[T]) -> T:
        pass
