from domain.model.Measure import DerivedMeasure, MeasurementMethod


class CyclomaticComplexity(DerivedMeasure[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__("Cyclomatic Complexity", "unit", 1.0, MeasurementMethod.AUTOMATIC, children, normalize_visitor,
                         aggregate_visitor)

    def copy(self, **kwargs):
        return CyclomaticComplexity(
            children=kwargs.get('children', self.children),
            normalize_visitor=self.normalize_visitor,
            aggregate_visitor=self.aggregate_visitor
        )
