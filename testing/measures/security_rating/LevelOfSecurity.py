from domain.model.Measure import BaseMeasure, MeasurementMethod


class LevelOfSecurity(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Level of Security", "grade", 1, MeasurementMethod.AUTOMATIC, visitor)
