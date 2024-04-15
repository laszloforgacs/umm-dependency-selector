from domain.model.Measure import BaseMeasure


class UpdatedIssuesCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("UpdatedIssuesCount", "updated issue", 1, visitor)