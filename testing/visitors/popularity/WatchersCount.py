from domain.model.Measure import BaseMeasure, MeasurementMethod


class WatchersCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Watchers Count", "watcher(s)", 1, MeasurementMethod.AUTOMATIC, visitor)
