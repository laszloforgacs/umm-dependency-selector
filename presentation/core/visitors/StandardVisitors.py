import asyncio

from presentation.core.visitors.Visitor import NormalizeVisitor, AggregateVisitor, BaseMeasureVisitor


class StandardNormalizeVisitor(NormalizeVisitor[float]):
    def normalize(self, measurements: list[float]) -> list[float]:
        total = sum(measurements)
        return [m / total for m in measurements]


class AverageAggregateVisitor(AggregateVisitor[float]):
    def aggregate(self, normalized_measures: list[float]) -> float:
        return sum(normalized_measures) / len(normalized_measures)


class MockMeasureVisitor(BaseMeasureVisitor[float]):
    async def measure(self, measure: 'BaseMeasure', repository: str) -> float:
        await asyncio.sleep(1)
        return 7438.0
