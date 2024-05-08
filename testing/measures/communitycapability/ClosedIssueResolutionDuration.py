from domain.model.Measure import BaseMeasure


class ClosedIssueResolutionDuration(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Closed Issue Resolution Duration", "issue", 1, visitor=visitor)