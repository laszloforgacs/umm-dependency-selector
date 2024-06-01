from domain.model.Measure import BaseMeasure, MeasurementMethod


class ReviewsAcceptedRatio(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Reviews Accepted - Total PR Ratio", "pull request", 1, MeasurementMethod.AUTOMATIC, visitor)