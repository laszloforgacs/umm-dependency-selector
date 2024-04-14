from domain.model.Measure import BaseMeasure


class OpenFeatureRequestCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("OpenFeatureRequestCount", "open issue with feature request label", 1, visitor)