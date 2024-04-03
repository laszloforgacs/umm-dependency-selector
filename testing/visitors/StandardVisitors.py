import asyncio
import random
from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import NormalizeVisitor, AggregateVisitor, BaseMeasureVisitor, T


class NoOpNormalizeVisitor(NormalizeVisitor[tuple[Measure, float]]):
    def normalize(self, measurements: list[tuple[Measure, float]]) -> list[tuple[Measure, float]]:
        return measurements


class StandardNormalizeVisitor(NormalizeVisitor[tuple[Measure, float]]):
    def normalize(self, measurements: list[tuple[Measure, float]]) -> list[tuple[Measure, float]]:
        total = sum(measurement_value for _, measurement_value in measurements)
        return [(measure, measure / total) for measure, _ in measurements]


class AverageAggregateVisitor(AggregateVisitor[tuple[Measure, float]]):
    def aggregate(self, normalized_measures: list[tuple[Measure, float]]) -> float:
        total = sum(measurement_value for _, measurement_value in normalized_measures)
        return total / len(normalized_measures)


class AddAggregateVisitor(AggregateVisitor[tuple[Measure, int | float]]):
    def aggregate(self, normalized_measures: list[tuple[Measure, int | float]]) -> float:
        total = sum(measurement_value for _, measurement_value in normalized_measures)
        return total


class MockMeasureVisitor(BaseMeasureVisitor[float]):
    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        random_top = random.uniform(10.0, 1000.0)
        rand = random.uniform(0.0, random_top)
        print(f"{repository.full_name}: {measure.name} is {rand}")
        return rand
