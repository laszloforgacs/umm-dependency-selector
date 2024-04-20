from domain.model.Measure import BaseMeasure, MeasurementMethod


class DeclinedIssueCount(BaseMeasure[int]):
    def __init__(
            self,
            visitor=None
    ):
        super().__init__(
            "Declined Issue Count",
            "issue",
            1,
            MeasurementMethod.AUTOMATIC,
            visitor
        )