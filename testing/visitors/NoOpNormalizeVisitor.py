from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import NormalizeVisitor


class NoOpNormalizeVisitor(NormalizeVisitor[tuple[Measure, float]]):
    def normalize(self, measurements: list[tuple[Measure, float]]) -> list[tuple[Measure, float]]:
        return measurements
