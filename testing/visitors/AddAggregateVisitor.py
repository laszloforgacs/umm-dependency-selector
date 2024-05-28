from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor


class AddAggregateVisitor(AggregateVisitor[tuple[Measure, int | float]]):
    def aggregate(self, normalized_measures: list[tuple[Measure, int | float]]) -> float:
        total = sum(measurement_value for _, measurement_value in normalized_measures)
        return total