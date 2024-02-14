from model.Result import Result, Success
from model.measurement.Measure import BaseMeasure, MeasurementMethod


class NumberOfStatements(BaseMeasure):
    def __init__(self):
        super().__init__("Number of statements", "statements", 1, MeasurementMethod.AUTOMATIC)

    def run(self) -> Result:
        return self.measure()

    def measure(self) -> Result:
        return Success(
            value = 399
        )