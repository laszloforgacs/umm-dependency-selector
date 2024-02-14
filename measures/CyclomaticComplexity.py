from model.Result import Result
from model.measurement.Measure import DerivedMeasure, MeasurementMethod


class CyclomaticComplexity(DerivedMeasure):
    def __init__(self):
        super().__init__("Cyclomatic Complexity", "unit", 1.0, MeasurementMethod.AUTOMATIC, {})

    def measure(self) -> list[Result]:
        return [
            child.measure() for child in self.children.values()
        ]