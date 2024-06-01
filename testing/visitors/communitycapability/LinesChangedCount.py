from domain.model.Measure import BaseMeasure, MeasurementMethod


class LinesChangedCount(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Total number of line changes", "line", 1, MeasurementMethod.AUTOMATIC, visitor)
