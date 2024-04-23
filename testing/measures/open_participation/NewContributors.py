from domain.model.Measure import BaseMeasure, MeasurementMethod


class NewContributors(BaseMeasure[int]):
    def __init__(
            self,
            visitor=None
    ):
        super().__init__(
            "New Contributors",
            "contributor(s)",
            1.0,
            MeasurementMethod.AUTOMATIC,
            visitor
        )
