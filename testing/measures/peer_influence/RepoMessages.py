from domain.model.Measure import BaseMeasure, MeasurementMethod


class RepoMessages(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Repo Messages", "comment(s)", 1, MeasurementMethod.AUTOMATIC, visitor)