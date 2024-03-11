from domain.model.Measure import DerivedMeasure, MeasurementMethod


class CyclomaticComplexity(DerivedMeasure[float]):
    def __init__(self):
        super().__init__("Cyclomatic Complexity", "unit", 1.0, MeasurementMethod.AUTOMATIC, {})

    def normalize(self, measurements: list[float]) -> list[float]:
        return [
            measurement / sum(measurements) for measurement in measurements
        ]

    def aggregate(self, normalized_measures: list[float]) -> float:
        return sum(normalized_measures) / len(normalized_measures)
