from domain.model.Measure import MeasurementMethod, DerivedMeasure


class CruzCodeQualityDerivedMeasure(DerivedMeasure[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Cruz Code Quality Derived Measure",
            "LOC/Comment ratio",
            1.0,
            MeasurementMethod.AUTOMATIC,
            children,
            normalize_visitor,
            aggregate_visitor
        )

    def copy(self, **kwargs):
        return CruzCodeQualityDerivedMeasure(
            children=kwargs.get('children', self.children),
            normalize_visitor=self.normalize_visitor,
            aggregate_visitor=self.aggregate_visitor
        )
