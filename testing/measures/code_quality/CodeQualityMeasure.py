from domain.model.Measure import BaseMeasure, MeasurementMethod


class CodeQualityMeasure(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Code Quality Measure", "value", 1, MeasurementMethod.AUTOMATIC, visitor)
