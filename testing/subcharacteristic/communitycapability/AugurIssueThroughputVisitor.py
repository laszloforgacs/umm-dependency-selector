from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor
from testing.visitors.communitycapability.ClosedIssuesCount import ClosedIssuesCount
from testing.visitors.communitycapability.TotalIssuesCount import TotalIssuesCount


class AugurIssueThroughputVisitor(AggregateVisitor[tuple[Measure, int]]):
    def __init__(self):
        super().__init__()

    def aggregate(self, normalized_measures: list[tuple[Measure, int]], repository: Repository) -> float:
        try:
            closed_issues_count = 0
            total_issues_count = 0
            for measure, measure_value in normalized_measures:
                if isinstance(measure, TotalIssuesCount):
                    total_issues_count += measure_value
                elif isinstance(measure, ClosedIssuesCount):
                    closed_issues_count += measure_value
            return closed_issues_count / total_issues_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)