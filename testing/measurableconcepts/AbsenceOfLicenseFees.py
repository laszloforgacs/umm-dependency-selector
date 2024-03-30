from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class AbsenceOfLicenseFees(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Absence of license fees",
            children,
            Impact.POSITIVE,
            "Software license",
            "Calculation of the absence of fees",
            "Absence of fees affects cost positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
