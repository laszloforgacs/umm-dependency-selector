from domain.model.Measure import BaseMeasure, MeasurementMethod


class FilesCount(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Count of files", "efficient", 1.0, MeasurementMethod.AUTOMATIC, visitor)