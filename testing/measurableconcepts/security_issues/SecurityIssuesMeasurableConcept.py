from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect

"""
Category 1 provided by Sonar.
"""


class SecurityIssuesMeasurableConcept(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Security Issues",
            children,
            Impact.NEGATIVE,
            "source code",
            "Measuring the number of total security issues in the source code",
            "Affects security negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
