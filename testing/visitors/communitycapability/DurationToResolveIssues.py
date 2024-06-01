from domain.model.Measure import BaseMeasure


class DurationToResolveIssues(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Closed Issue Resolution Duration", "issue(s)", 1, visitor=visitor)