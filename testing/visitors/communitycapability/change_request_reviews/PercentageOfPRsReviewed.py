from domain.model.Measure import BaseMeasure, MeasurementMethod


class PercentageOfPRsReviewed(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Percentage of PRs reviewed", "%", 1,
                         MeasurementMethod.AUTOMATIC, visitor)
