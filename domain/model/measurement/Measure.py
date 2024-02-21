from abc import ABC, ABCMeta, abstractmethod
from enum import Enum

from domain.model.Result import Result
from domain.model.components.Component import LeafComponent, CompositeComponent


class MeasurementMethod(Enum):
    AUTOMATIC = 1
    MANUAL = 2


class Measure(ABC):
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


class BaseMeasure(Measure, LeafComponent, metaclass=ABCMeta):
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

    @abstractmethod
    def measure(self) -> Result:
        pass


class DerivedMeasure(Measure, CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, unit: str, scale: float, measurement_method: MeasurementMethod,
                 children: dict[str, BaseMeasure]):
        self._name = name
        self._unit = unit
        self._scale = scale
        self._measurement_method = measurement_method
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

    @abstractmethod
    def measure(self) -> list[Result]:
        pass
