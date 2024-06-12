from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor


class AverageAggregateVisitor(AggregateVisitor[tuple[Measure, float]]):
    async def aggregate(self, normalized_measures: list[tuple[Measure, float]], repository: Repository) -> float:
        total = sum(measurement_value for _, measurement_value in normalized_measures)
        return total / len(normalized_measures)
