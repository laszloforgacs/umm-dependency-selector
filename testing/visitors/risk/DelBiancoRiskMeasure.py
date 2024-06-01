from domain.model.Measure import BaseMeasure


class DelBiancoRiskMeasure(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("DelBianco risk", "count", 1, visitor=visitor)
