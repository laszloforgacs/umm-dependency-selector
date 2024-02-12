from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.components.Component import Component


class Measurer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def measure(self, component: Component) -> Result:
        pass
