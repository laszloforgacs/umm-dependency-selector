from domain.model.Measure import DerivedMeasure, MeasurementMethod

"""
augur measure: Time series of number of declined reviews / pull requests opened within a certain period.
"""
class ReviewsDeclinedRatio(DerivedMeasure[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Reviews Declined - Total PR Ratio",
            "ratio",
            1.0,
            MeasurementMethod.AUTOMATIC,
            children,
            normalize_visitor,
            aggregate_visitor
        )