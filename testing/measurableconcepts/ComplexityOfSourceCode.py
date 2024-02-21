from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect
from domain.model.Result import Result, Success


class ComplexityOfSourceCode(MeasurableConcept):
    def __init__(self):
        super().__init__("Complexity of source code", {}, Impact.NEGATIVE, "Source code", OSSAspect.CODE,
                         "Calculation of source code complexity", "Affects Maintainability negatively")

    def run(self) -> Result:
        measurements = [result.value for result in self.measure()]
        return Success(
            value=sum(measurements) / len(measurements)
        )

    def measure(self) -> list[Result]:
        return [
            child.run() for child in self.children.values()
        ]
