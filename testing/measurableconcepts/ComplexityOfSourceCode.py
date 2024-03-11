from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect
from domain.model.Result import Result, Success


class ComplexityOfSourceCode(MeasurableConcept[float]):
    def __init__(self):
        super().__init__("Complexity of source code", {}, Impact.NEGATIVE, "Source code",
                         "Calculation of source code complexity", "Affects Maintainability negatively", OSSAspect.CODE)

    def normalize(self, measurements: list[float]) -> list[float]:
        return [
            measurement / sum(measurements) for measurement in measurements]

    def aggregate(self, normalized_measures: list[float]) -> float:
        return sum(normalized_measures) / len(normalized_measures)
