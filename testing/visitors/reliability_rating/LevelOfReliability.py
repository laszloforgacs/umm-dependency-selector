from domain.model.Measure import BaseMeasure, MeasurementMethod


class LevelOfReliability(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Level of Reliability", "grade", 1, MeasurementMethod.AUTOMATIC, visitor)
