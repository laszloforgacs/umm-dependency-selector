from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class ChangeRequestsAcceptedCount(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of Change Requests Accepted",
            children,
            Impact.POSITIVE,
            "pull requests in version control",
            "Calculating the number of pull requests that have been accepted in the version control history",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )