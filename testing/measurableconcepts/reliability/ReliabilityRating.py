from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class ReliabilityRating(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Reliability Rating",
            children,
            Impact.POSITIVE,
            "source code",
            "Calculating the reliability rating of a repository",
            "Reliability affects quality positively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
