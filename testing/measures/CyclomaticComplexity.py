from domain.model.Measure import DerivedMeasure, MeasurementMethod


class CyclomaticComplexity(DerivedMeasure[float]):
    def __init__(self, children):
        super().__init__("Cyclomatic Complexity", "unit", 1.0, MeasurementMethod.AUTOMATIC, children)
