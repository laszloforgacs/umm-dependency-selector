from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class ChangeRequestsDeclinedCount(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of Change Requests Declined",
            children,
            Impact.NEGATIVE,
            "pull requests in version control",
            "Calculating the number of pull requests that have been declined in the version control history",
            "Affects Community Capability negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )