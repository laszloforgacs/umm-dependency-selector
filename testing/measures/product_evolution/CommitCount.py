from domain.model.Measure import BaseMeasure


class CommitCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("CommitCount", "commit", 1, visitor)

    def __copy__(self):
        return CommitCount(
            visitor=self.visitor
        )