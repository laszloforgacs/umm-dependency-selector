from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class CodeChangesCommits(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Code Changes Commits",
            children,
            Impact.POSITIVE,
            "version control history",
            "Calculating the total number of commits in the version control history",
            "Affects Community Capability positively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )