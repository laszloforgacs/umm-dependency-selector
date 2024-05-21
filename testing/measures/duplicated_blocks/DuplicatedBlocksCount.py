from domain.model.Measure import BaseMeasure, MeasurementMethod


class DuplicatedBlocksCount(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Count of Duplicated Blocks", "block(s)", 1, MeasurementMethod.AUTOMATIC, visitor)
