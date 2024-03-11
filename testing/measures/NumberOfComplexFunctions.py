from domain.model.Measure import BaseMeasure, MeasurementMethod


class NumberOfComplexFunctions(BaseMeasure[float]):
    def __init__(self):
        super().__init__("Number of complex functions", "unit", 1.0, MeasurementMethod.AUTOMATIC)
