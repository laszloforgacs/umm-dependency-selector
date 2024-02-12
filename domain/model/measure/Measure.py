from abc import ABC, abstractmethod
from enum import Enum

from domain.model.Result import Result
from domain.model.components.Component import Component
from domain.model.components.CompositeComponent import CompositeComponent
from domain.model.components.LeafComponent import LeafComponent
from domain.model.measure.Measurer import Measurer


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


class BaseMeasure(Measure, LeafComponent):
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

    def add_component(self, component: Component):
        pass

    def remove_component(self, component: Component):
        pass

    def measure(self, measurer: Measurer) -> Result:
        return measurer.measure_leaf_component(self)


class DerivedMeasure(Measure, CompositeComponent):
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

    def measure(self, measurer: Measurer) -> Result:
        return measurer.measure_composite_component(self)
