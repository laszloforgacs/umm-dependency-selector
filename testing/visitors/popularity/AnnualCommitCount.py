from domain.model.Measure import BaseMeasure, MeasurementMethod


class AnnualCommitCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Annual Commit Count", "commit", 1, MeasurementMethod.AUTOMATIC, visitor)
