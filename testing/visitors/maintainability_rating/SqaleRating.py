from domain.model.Measure import BaseMeasure, MeasurementMethod


class SqaleRating(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Sqale Rating", "rating", 1, MeasurementMethod.AUTOMATIC, visitor)
