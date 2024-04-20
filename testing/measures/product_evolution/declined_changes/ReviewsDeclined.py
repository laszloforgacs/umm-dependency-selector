from domain.model.Measure import DerivedMeasure, MeasurementMethod

"""
augur measure: Time series of number of declined reviews / pull requests opened within a certain period.
"""
class ReviewsDeclined(DerivedMeasure[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Reviews declined",
            "ratio",
            1.0,
            MeasurementMethod.AUTOMATIC,
            children,
            normalize_visitor,
            aggregate_visitor
        )