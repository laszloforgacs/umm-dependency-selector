from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class OpenedPullRequests(MeasurableConcept[int]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Opened pull requests in a period",
            children,
            Impact.POSITIVE,
            "Issue history",
            "Calculating the number of opened pull requests",
            "Regular pull requests affect product evolution positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )