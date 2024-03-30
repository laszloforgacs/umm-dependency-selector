from domain.model.Measure import BaseMeasure


class License(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("License", "levels", 1, visitor)
