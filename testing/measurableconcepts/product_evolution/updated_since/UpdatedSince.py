from domain.model.MeasureableConcept import MeasurableConcept, Impact

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
            Impact.POSITIVE,
            "Commit history",
            "Calculation of the time since the last commit",
            "Regular updates affect product evolution positively",
            normalize_visitor,
            aggregate_visitor
        )