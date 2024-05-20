from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class SoftwareQuality(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Software Quality",
            children,
            Impact.POSITIVE,
            "source code",
            "Measuring software quality",
            "Affects overall quality of the project positively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )