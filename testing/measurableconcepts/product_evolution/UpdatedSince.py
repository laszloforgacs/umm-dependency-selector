from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect

"""
criticality_score metric.
"""
class UpdatedSince(MeasurableConcept[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Updated since",
            children,
            Impact.NEGATIVE,
            "Commit history",
            "Calculation of the time since the last commit",
            "Non-regular updates affect product evolution negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )