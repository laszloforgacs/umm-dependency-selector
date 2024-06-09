from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import NormalizeVisitor


class StandardNormalizeVisitor(NormalizeVisitor[tuple[Measure, float]]):
    def normalize(self, measurements: list[tuple[Measure, float]], repository: Repository) -> list[tuple[Measure, float]]:
        total = sum(measurement_value for _, measurement_value in measurements)
        return [(measure, measure / total) for measure, _ in measurements]
