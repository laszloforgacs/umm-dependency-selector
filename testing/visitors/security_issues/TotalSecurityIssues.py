from domain.model.Measure import BaseMeasure, MeasurementMethod


class TotalSecurityIssues(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Number of Security Issues", "total issues", 1, MeasurementMethod.AUTOMATIC, visitor)
