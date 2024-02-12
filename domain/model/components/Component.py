from abc import ABC, abstractmethod

from domain.model.aggregation.Aggregatable import Aggregatable
from domain.model.measure.Measurable import Measurable
from domain.model.normalization.Normalizable import Normalizable


class Component(ABC, Measurable, Aggregatable, Normalizable):

    @abstractmethod
    def __init__(self):
        pass

    @property.getter
    @abstractmethod
    def name(self) -> str:
        pass

    @property.getter
    @abstractmethod
    def children(self) -> dict:
        pass

    @abstractmethod
    def add_component(self, component: Component):
        """
        add_component adds a component to the component map
        """
        pass

    @abstractmethod
    def remove_component(self, component: Component):
        """
        remove_component removes a component from the component map
        """
        pass
