from domain.model.Measure import BaseMeasure, MeasurementMethod


class AvgGunningFogIndex(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Average Gunning Fog Index", "value", 1, MeasurementMethod.AUTOMATIC, visitor)
