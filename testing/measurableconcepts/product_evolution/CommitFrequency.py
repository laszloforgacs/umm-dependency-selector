from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class CommitFrequency(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Commit Frequency",
            children,
            Impact.POSITIVE,
            "Commit",
            "Calculation of the average commits in a specified date range",
            "Commit frequency affects reliability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
