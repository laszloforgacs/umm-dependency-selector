from domain.model.Measure import BaseMeasure, MeasurementMethod


class ClassesCount(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Count of classes", "efficient", 1.0, MeasurementMethod.AUTOMATIC, visitor)