from domain.model.Measure import BaseMeasure, MeasurementMethod


class ReviewsDeclinedCount(BaseMeasure[int]):
    def __init__(
            self,
            visitor=None
    ):
        super().__init__(
            "Reviews Declined Count",
            "issue",
            1,
            MeasurementMethod.AUTOMATIC,
            visitor
        )