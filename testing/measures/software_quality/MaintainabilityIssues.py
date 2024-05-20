from domain.model.Measure import BaseMeasure, MeasurementMethod


class MaintainabilityIssues(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Number of Maintainability issues", "total issues", 1, MeasurementMethod.AUTOMATIC, visitor)
