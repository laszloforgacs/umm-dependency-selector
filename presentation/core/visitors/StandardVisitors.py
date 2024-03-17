import asyncio
import random

from presentation.core.visitors.Visitor import NormalizeVisitor, AggregateVisitor, BaseMeasureVisitor, T


class NoOpNormalizeVisitor(NormalizeVisitor[float]):
    def normalize(self, measurements: list[float]) -> list[float]:
        return measurements


class StandardNormalizeVisitor(NormalizeVisitor[float]):
    def normalize(self, measurements: list[float]) -> list[float]:
        total = sum(measurements)
        return [measure / total for measure in measurements]


class AverageAggregateVisitor(AggregateVisitor[float]):
    def aggregate(self, normalized_measures: list[float]) -> float:
        return sum(normalized_measures) / len(normalized_measures)


class MockMeasureVisitor(BaseMeasureVisitor[float]):
    async def measure(self, measure: 'BaseMeasure', repository: str) -> float:
        random_top = random.uniform(10.0, 1000.0)
        rand = random.uniform(0.0, random_top)
        print(f"{repository.full_name}: {measure.name} is {rand}")
        await asyncio.sleep(0.1)
        return rand
