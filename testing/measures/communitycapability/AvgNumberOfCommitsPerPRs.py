from domain.model.Measure import BaseMeasure, MeasurementMethod


class AvgNumberOfCommitsPerPRs(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Avg number of commits per pull requests", "commit(s)", 1, MeasurementMethod.AUTOMATIC, visitor)
