from domain.model.Measure import BaseMeasure


class TotalIssuesCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Number of total issues", "issue", 1, visitor)