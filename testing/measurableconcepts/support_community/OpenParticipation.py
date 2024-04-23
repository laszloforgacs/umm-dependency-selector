from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect, Impact


class OpenParticipation(MeasurableConcept[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Open Participation",
            children,
            Impact.POSITIVE,
            "Issue tracker",
            "Calculating the level of collaboration in the issue tracker",
            "Open participation affects a supportive community positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
