from domain.model.Measure import BaseMeasure


class ClosedIssuesCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Number of closed issues", "issue", 1, visitor)
