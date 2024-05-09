from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
Augur: Closed Issue Resolution Duration
CHAOSS: Issue Resolution Duration
Category 1
"""


class IssueResolutionDurationAverage(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Average Duration to Resolve Issues",
            children,
            Impact.NEGATIVE,
            "issues in issue tracker",
            "Calculating the duration to resolve issues",
            "Longer durations to resolve issues affect community capability/product evolution negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
