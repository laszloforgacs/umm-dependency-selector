from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor
from testing.visitors.CruzNumberOfCommentsBaseMeasure import CruzNumberOfCommentsBaseMeasure
from testing.visitors.LinesOfCode import LinesOfCode


class CruzCodeQualityDerivedMeasureAggregator(AggregateVisitor[tuple[Measure, float]]):
    def __init__(self):
        super().__init__()

    async def aggregate(self, normalized_measures: list[tuple[Measure, float]], repository: Repository) -> float:
        lines_of_code = 0.0
        comments = 0.0

        for measure, measure_value in normalized_measures:
            if isinstance(measure, LinesOfCode):
                lines_of_code += measure_value
            elif isinstance(measure, CruzNumberOfCommentsBaseMeasure):
                comments += measure_value

        if comments == 0 or lines_of_code == 0:
            return 0.0

        ratio = comments / lines_of_code

        if ratio <= 0.10:
            return 2.0
        elif ratio <= 0.25:
            return 2.0 + ((ratio - 0.10) * (1.0 / (0.25 - 0.10)))
        else:
            return 3.0
