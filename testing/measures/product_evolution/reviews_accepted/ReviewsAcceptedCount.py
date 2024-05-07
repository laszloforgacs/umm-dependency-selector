from domain.model.Measure import BaseMeasure, MeasurementMethod


class ReviewsAcceptedCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Reviews Accepted Count", "pull request(s)", 1, MeasurementMethod.AUTOMATIC, visitor)