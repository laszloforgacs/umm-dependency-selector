from domain.model.Measure import BaseMeasure, MeasurementMethod


class ForksCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Forks Count", "fork(s)", 1, MeasurementMethod.AUTOMATIC, visitor)
