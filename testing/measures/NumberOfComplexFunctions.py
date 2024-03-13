from domain.model.Measure import BaseMeasure, MeasurementMethod


class NumberOfComplexFunctions(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Number of complex functions", "unit", 1.0, MeasurementMethod.AUTOMATIC, visitor=visitor)

    def copy(self):
        return NumberOfComplexFunctions(
            visitor=self.visitor
        )