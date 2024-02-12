from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.components.CompositeComponent import CompositeComponent
from domain.model.components.LeafComponent import LeafComponent


class Normalizer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def normalize_composite_component(self, composite_component: CompositeComponent) -> Result:
        pass

    @abstractmethod
    def normalize_leaf_component(self, leaf_component: LeafComponent) -> Result:
        pass
