from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class AvgLengthOfFunctions(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Average Length of Functions",
            children,
            Impact.NEGATIVE,
            "source code",
            "Calculating the average number lines of code per function in the source code",
            "Affects project size negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )