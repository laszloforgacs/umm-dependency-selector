from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect
from domain.model.Result import Result, Success


class ComplexityOfSourceCode(MeasurableConcept[float]):
    def __init__(self, children):
        super().__init__("Complexity of source code", children, Impact.NEGATIVE, "Source code",
                         "Calculation of source code complexity", "Affects Maintainability negatively", OSSAspect.CODE)
