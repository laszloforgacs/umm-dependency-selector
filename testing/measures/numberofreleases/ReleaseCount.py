from domain.model.Measure import BaseMeasure


class ReleaseCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Number of Releases", "release", 1, visitor)

    def __copy__(self):
        return ReleaseCount(
            visitor=self.visitor
        )