from domain.model.Measure import BaseMeasure


class ContributorCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Contributor count", "person", 1, visitor=visitor)