from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class ChangeRequestsDeclinedRatio(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Ratio of Change Requests Declined",
            children,
            Impact.NEGATIVE,
            "pull requests in version control",
            "Calculating the declined pull requests to total pull requests ratio in the version control history",
            "Affects Community Capability negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )