from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class TimeToRespondToIssues(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Time to Respond to Issues",
            children,
            Impact.NEGATIVE,
            "issue",
            "Calculating the first response time to issues",
            "Affects Community Capability negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )