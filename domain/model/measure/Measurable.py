from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.measure.Measurer import Measurer


class Measurable(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def measure(self, measurer: Measurer) -> Result:
        pass
