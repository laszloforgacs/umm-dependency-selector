from model.Result import Result, Success
from model.measurement.Measure import BaseMeasure, MeasurementMethod


class LinesOfCode(BaseMeasure):
    def __init__(self):
        super().__init__("Lines of Code", "unit", 1.0, MeasurementMethod.AUTOMATIC)

    def measure(self) -> Result:
        return Success(
            value = 39821048
        )