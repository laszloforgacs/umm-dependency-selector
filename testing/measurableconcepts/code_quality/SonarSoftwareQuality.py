from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect

"""
Since this is comprised of MaintainabilityIssues, ReliabilityRemediationEffort, and SecurityRemediationEffort
that sonar considers as negative, the overall impact of this concept is negative.
"""


class SonarSoftwareQuality(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Sonar Software Quality",
            children,
            Impact.NEGATIVE,
            "source code",
            "Measuring software quality",
            "Affects overall quality of the project negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
