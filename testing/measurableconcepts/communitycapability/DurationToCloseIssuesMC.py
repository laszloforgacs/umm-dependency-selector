from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
Augur: Closed Issue Resolution Duration
CHAOSS: Change Requests Duration
Category 1
"""


class DurationToCloseIssuesMC(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Duration to Close Issues",
            children,
            Impact.NEGATIVE,
            "issue",
            "Calculating the duration to close issues",
            "Affects Community Capability negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
