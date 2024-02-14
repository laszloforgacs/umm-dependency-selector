from model.Result import Success, Result
from model.measurement.Measure import BaseMeasure, MeasurementMethod


class NumberOfComplexFunctions(BaseMeasure):
    def __init__(self):
        super().__init__("Number of complex functions", "unit", 1.0, MeasurementMethod.AUTOMATIC)

    def run(self) -> Result:
        return self.measure()

    def measure(self) -> Result:
        return Success(
            value=39821048
        )
