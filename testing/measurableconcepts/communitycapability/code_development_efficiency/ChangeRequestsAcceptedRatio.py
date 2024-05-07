from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class ChangeRequestsAcceptedRatio(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Ratio of Change Requests Accepted",
            children,
            Impact.POSITIVE,
            "pull requests in version control",
            "Calculating the accepted pull requests to total pull requests ratio in the version control history",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )