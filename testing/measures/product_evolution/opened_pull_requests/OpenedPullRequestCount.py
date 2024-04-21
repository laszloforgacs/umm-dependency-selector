from domain.model.Measure import BaseMeasure, MeasurementMethod


class OpenedPullRequestCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__(
            "Number of opened pull requests",
            "pull request",
            1,
            MeasurementMethod.AUTOMATIC,
            visitor
        )