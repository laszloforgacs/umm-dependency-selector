from model.Result import Result, Success
from model.measurement.Measure import DerivedMeasure, MeasurementMethod


class CyclomaticComplexity(DerivedMeasure):
    def __init__(self):
        super().__init__("Cyclomatic Complexity", "unit", 1.0, MeasurementMethod.AUTOMATIC, {})

    def run(self) -> Result:
        measures = [result.value for result in self.measure()]
        normalized = self.normalize(measures)
        return Success(
            value=self.aggregate(normalized)
        )

    def measure(self) -> list[Result]:
        return [
            child.measure() for child in self.children.values()
        ]

    def aggregate(self, normalizedResults: list[float]) -> float:
        return sum(normalizedResults) / len(normalizedResults)

    def normalize(self, measuredResults: list[float]) -> list[float]:
        total = sum(measuredResults)
        return [
            result / total for result in measuredResults
        ]
