from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.aggregation.Aggregator import Aggregator
from domain.model.components.Component import Component
from domain.model.measure.Measurer import Measurer
from domain.model.normalization.Normalizer import Normalizer


class CompositeComponent(ABC, Component):
    @abstractmethod
    def __init__(self):
        pass

    def add_component(self, component: Component):
        self._children[component.name] = component.children

    def remove_component(self, component: Component):
        del self.children[component.name]

    @abstractmethod
    def measure(self, measurer: Measurer) -> Result:
        pass

    @abstractmethod
    def aggregate(self, aggregator: Aggregator) -> Result:
        pass

    @abstractmethod
    def normalize(self, normalizer: Normalizer) -> Result:
        pass
