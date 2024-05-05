from domain.model.Measure import BaseMeasure, MeasurementMethod


class DownloadsCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Downloads Count", "download(s)", 1, MeasurementMethod.AUTOMATIC, visitor)
