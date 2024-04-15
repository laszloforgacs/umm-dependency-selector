from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class IssueUpdates(MeasurableConcept[int]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Issue updates",
            children,
            Impact.POSITIVE,
            "Issue history",
            "Calculating the level of interaction with issues",
            "Regular updates affect product evolution positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )