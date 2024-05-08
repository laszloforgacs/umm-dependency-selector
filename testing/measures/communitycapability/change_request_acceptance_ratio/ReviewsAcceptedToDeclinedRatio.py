from domain.model.Measure import DerivedMeasure, MeasurementMethod

"""
CHAOSS measure: Ratio of reviews accepted to reviews declined
"""


class ReviewsAcceptedToDeclinedRatio(DerivedMeasure[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Reviews Accepted to Reviews Declined Ratio",
            "ratio",
            1.0,
            MeasurementMethod.AUTOMATIC,
            children,
            normalize_visitor,
            aggregate_visitor
        )
