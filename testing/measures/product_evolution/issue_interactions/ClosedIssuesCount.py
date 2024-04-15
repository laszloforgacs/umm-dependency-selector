from domain.model.Measure import BaseMeasure


class ClosedIssuesCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("ClosedIssueCount", "closed issue", 1, visitor)