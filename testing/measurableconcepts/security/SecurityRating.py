from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class SecurityRating(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Security Rating",
            children,
            Impact.POSITIVE,
            "source code",
            "Calculating the security rating of a repository",
            "Security affects quality positively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
