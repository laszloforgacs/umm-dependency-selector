from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.aggregation.Aggregator import Aggregator
from domain.model.components.Component import Component
from domain.model.measure.Measurer import Measurer
from domain.model.normalization.Normalizer import Normalizer


class LeafComponent(ABC, Component):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_component(self, component: Component):
        pass

    @abstractmethod
    def remove_component(self, component: Component):
        pass

    @abstractmethod
    def measure(self, measurer: Measurer) -> Result:
        pass

    @abstractmethod
    def aggregate(self, aggregator: Aggregator) -> Result:
        pass

    @abstractmethod
    def normalize(self, normalizer: Normalizer) -> Result:
        pass
