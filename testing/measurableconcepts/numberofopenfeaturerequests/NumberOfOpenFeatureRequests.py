from domain.model.MeasureableConcept import Impact, OSSAspect, MeasurableConcept


class NumberOfOpenFeatureRequests(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of open feature requests",
            children,
            Impact.NEGATIVE,
            "Feature request",
            "Calculation of the number of open feature requests",
            "Number of open feature requests affects reliability negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )