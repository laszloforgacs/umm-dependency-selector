from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class CodeChangesLines(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Code Changes Lines",
            children,
            Impact.NEGATIVE,
            "source code",
            "Calculating the total number of lines changed in the source code",
            "Affects Community Capability negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )