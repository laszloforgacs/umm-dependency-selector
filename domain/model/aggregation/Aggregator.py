from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.components.CompositeComponent import CompositeComponent
from domain.model.components.LeafComponent import LeafComponent


class Aggregator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def aggregate_composite_component(self, composite_component: CompositeComponent) -> Result:
        pass

    @abstractmethod
    def aggregate_leaf_component(self, leaf_component: LeafComponent) -> Result:
        pass
