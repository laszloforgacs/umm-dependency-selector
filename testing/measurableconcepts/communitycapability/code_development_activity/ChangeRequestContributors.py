from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class ChangeRequestContributors(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Change Request Contributors",
            children,
            Impact.POSITIVE,
            "pull requests in version control",
            "Calculating the average number of contributors per pull request in the version control history",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
