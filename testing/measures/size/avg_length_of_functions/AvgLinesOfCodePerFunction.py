from domain.model.Measure import BaseMeasure, MeasurementMethod


class AvgLinesOfCodePerFunction(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Avg Lines of Code per Function", "lines", 1, MeasurementMethod.AUTOMATIC, visitor)
