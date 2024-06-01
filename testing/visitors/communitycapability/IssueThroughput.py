from domain.model.Measure import MeasurementMethod, DerivedMeasure


class IssueThroughput(DerivedMeasure[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Issue Throughput",
            "issue",
            1.0,
            MeasurementMethod.AUTOMATIC,
            children,
            normalize_visitor,
            aggregate_visitor
        )