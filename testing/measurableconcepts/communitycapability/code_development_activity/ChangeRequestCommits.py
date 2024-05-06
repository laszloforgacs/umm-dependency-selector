from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class ChangeRequestCommits(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Change Request Commits",
            children,
            Impact.NEGATIVE,
            "pull requests in version control",
            "Calculating the average number of commits per pull request in the version control history",
            "Affects Community Capability negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )