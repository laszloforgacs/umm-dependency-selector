from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect, Impact


class SharedSupport(MeasurableConcept[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Shared support",
            children,
            Impact.POSITIVE,
            "Issue tracker",
            "Calculating the level of collaboration in the issue tracker",
            "Shared support affects a supportive community positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )