from domain.model.Measure import BaseMeasure, MeasurementMethod


class DurationToResolvePullRequests(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Duration to Resolve Pull Requests", "pull request(s)", 1, MeasurementMethod.AUTOMATIC, visitor=visitor)