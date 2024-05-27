from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class MaintainabilityRating(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Maintainability Rating",
            children,
            Impact.POSITIVE,
            "source code",
            "Calculating the maintainability rating of a repository",
            "Maintainability affects quality positively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
