from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from domain.model.ABCGenericMeta import ABCGenericMeta

T = TypeVar('T')


class Visitor(Generic[T], metaclass=ABCGenericMeta):
    @abstractmethod
    def __init__(self):
        pass


class NormalizeVisitor(Visitor[T]):
    def __init__(self):
        pass

    @abstractmethod
    def normalize(self, measurements: list[tuple['Measure', T]]) -> list[T]:
        pass


class AggregateVisitor(Visitor[T]):
    def __init__(self):
        pass

    @abstractmethod
    def aggregate(self, normalized_measures: list[tuple['Measure', T]]) -> T:
        pass


class BaseMeasureVisitor(Visitor[T]):
    def __init__(self):
        pass

    @abstractmethod
    async def measure(self, measure: 'BaseMeasure', repository: str) -> T:
        pass
