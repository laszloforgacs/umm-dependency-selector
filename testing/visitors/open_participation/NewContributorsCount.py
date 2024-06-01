from domain.model.Measure import BaseMeasure, MeasurementMethod

"""
CHAOSS, Category 1
"""


class NewContributorsCount(BaseMeasure[int]):
    def __init__(
            self,
            visitor=None
    ):
        super().__init__(
            "New Contributors Count",
            "contributor(s)",
            1.0,
            MeasurementMethod.AUTOMATIC,
            visitor
        )
