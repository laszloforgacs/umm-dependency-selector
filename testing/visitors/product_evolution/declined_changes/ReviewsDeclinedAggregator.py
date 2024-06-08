from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor
from testing.visitors.communitycapability.TotalIssuesCount import TotalIssuesCount
from testing.visitors.product_evolution.declined_changes.ReviewsDeclinedCount import ReviewsDeclinedCount


class ReviewsDeclinedAggregator(AggregateVisitor[tuple[Measure, int]]):
    def __init__(self):
        super().__init__()

    def aggregate(self, normalized_measures: list[tuple[Measure, int]], repository: Repository) -> float:
        declined_issues = 0
        total_issues = 0

        for measure, measure_value in normalized_measures:
            if isinstance(measure, TotalIssuesCount):
                total_issues += measure_value
            if isinstance(measure, ReviewsDeclinedCount):
                declined_issues += measure_value

        if total_issues == 0:
            print(f"Declined issues: {declined_issues}, Total issues: {total_issues}, Ratio: {declined_issues}")
            return declined_issues

        ratio = declined_issues / total_issues
        print(f"Declined issues: {declined_issues}, Total issues: {total_issues}, Ratio: {ratio}")
        return ratio