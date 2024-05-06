from domain.model.Measure import BaseMeasure, MeasurementMethod


class AvgNumberOfContributorsPerPRs(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Avg number of contributors per pull requests", "contributor(s)", 1,
                         MeasurementMethod.AUTOMATIC, visitor)
