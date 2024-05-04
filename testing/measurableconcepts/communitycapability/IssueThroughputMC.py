from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class IssueThroughputMC(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Issue Throughput",
            children,
            Impact.POSITIVE,
            "issues",
            "Calculating the throughput of issues",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )