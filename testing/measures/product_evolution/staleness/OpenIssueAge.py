from domain.model.Measure import BaseMeasure


class OpenIssueAge(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Open Issue Age", "day(s)", 1, visitor)