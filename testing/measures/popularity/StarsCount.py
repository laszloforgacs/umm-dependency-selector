from domain.model.Measure import BaseMeasure, MeasurementMethod


class StarsCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Stars Count", "star(s)", 1, MeasurementMethod.AUTOMATIC, visitor)
