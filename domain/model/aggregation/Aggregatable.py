from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.aggregation import Aggregator


class Aggregatable(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def aggregate(self, aggregator: Aggregator) -> Result:
        pass
