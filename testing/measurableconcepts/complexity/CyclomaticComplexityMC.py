from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class CyclomaticComplexityMC(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Cyclomatic Complexity",
            children,
            Impact.NEGATIVE,
            "soure code",
            "Calculating the cyclomatic complexity of the project",
            "Affects 'Complexity' negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )