<<<<<<< HEAD
from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect
=======
from domain.model.MeasureableConcept import MeasurableConcept, Impact
>>>>>>> 60a1aa6853d16b0e7f10b0c1c4107c1ec2f1cbed


class AbsenceOfLicenseFees(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Absence of license fees",
            children,
            Impact.POSITIVE,
            "Software license",
            "Calculation of the absence of fees",
            "Absence of fees affects cost positively",
            normalize_visitor,
            aggregate_visitor
        )
