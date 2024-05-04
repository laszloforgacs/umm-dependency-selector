from domain.model.Measure import BaseMeasure, MeasurementMethod


class ClosedIssuesCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Number of closed issues", "issue", 1, MeasurementMethod.AUTOMATIC, visitor)
