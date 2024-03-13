from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect
from domain.model.Result import Result, Success


class ComplexityOfSourceCode(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__("Complexity of source code", children, Impact.NEGATIVE, "Source code",
                         "Calculation of source code complexity", "Affects Maintainability negatively", OSSAspect.CODE, normalize_visitor, aggregate_visitor)

    def copy(self, **kwargs):
        return ComplexityOfSourceCode(
            children=kwargs.get('children', self.children),
            normalize_visitor=self.normalize_visitor,
            aggregate_visitor=self.aggregate_visitor
        )


class ComplexityOfSourceCode2(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__("Complexity of source code2", children, Impact.NEGATIVE, "Source code",
                         "Calculation of source code complexity", "Affects Maintainability negatively",
                         OSSAspect.COMMUNITY, normalize_visitor, aggregate_visitor)

    def copy(self, **kwargs):
        return ComplexityOfSourceCode2(
            children=kwargs.get('children', self.children),
            normalize_visitor=self.normalize_visitor,
            aggregate_visitor=self.aggregate_visitor
        )