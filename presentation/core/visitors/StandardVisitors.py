import asyncio
import random

from presentation.core.visitors.Visitor import NormalizeVisitor, AggregateVisitor, BaseMeasureVisitor, T


class NoOpNormalizeVisitor(NormalizeVisitor[float]):
    def normalize(self, measurements: list[tuple['Measure', float]]) -> list[float]:
        return measurements


class StandardNormalizeVisitor(NormalizeVisitor[float]):
    def normalize(self, measurements: list[tuple['Measure', float]]) -> list[float]:
        values = [m[1] for m in measurements]
        total = sum(values)
        return [m / total for m in values]


class AverageAggregateVisitor(AggregateVisitor[float]):
    def aggregate(self, normalized_measures: list[tuple['Measure', float]]) -> float:
        values = [m[1] for m in normalized_measures]
        return sum(values) / len(values)


class MockMeasureVisitor(BaseMeasureVisitor[float]):
    async def measure(self, measure: 'BaseMeasure', repository: str) -> float:
        random_top = random.uniform(10.0, 1000.0)
        rand = random.uniform(0.0, random_top)
        print(f"{repository}: {measure.name} is {rand}")
        await asyncio.sleep(1)
        return rand
