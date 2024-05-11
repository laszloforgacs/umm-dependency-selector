from domain.model.Measure import MeasurementMethod, DerivedMeasure

"""
from CHAOSS. belongs to Comunity Growth, New Contributors Closing Issues
Category 1 measure
Analyzed in the last 3 months
"""


class ClosedIssuesCountByNewContributors(DerivedMeasure[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of issues closed by new contributors",
            "issue(s)",
            1.0,
            MeasurementMethod.AUTOMATIC,
            children,
            normalize_visitor,
            aggregate_visitor
        )
