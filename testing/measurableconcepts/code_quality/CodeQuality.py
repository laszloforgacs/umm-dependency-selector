from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class CodeQuality(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Code Quality",
            children,
            Impact.POSITIVE,
            "source code",
            "Measuring code quality",
            "Affects overall quality of the project positively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )