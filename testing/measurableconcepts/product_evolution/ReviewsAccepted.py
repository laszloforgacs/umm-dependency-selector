from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect, Impact


class ReviewsAccepted(MeasurableConcept[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Reviews accepted",
            children,
            Impact.POSITIVE,
            "Pull request history",
            "Ratio of accepted reviews to total reviews",
            "Regularly accepted reviews affect product evolution positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )