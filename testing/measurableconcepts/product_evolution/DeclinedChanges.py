from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class DeclinedChanges(MeasurableConcept[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Declined changes",
            children,
            Impact.NEGATIVE,
            "Issue history",
            "Calculating the ratio of declined changes to accepted PRs",
            "Declined changes affect product evolution negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
