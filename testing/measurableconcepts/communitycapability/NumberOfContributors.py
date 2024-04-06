from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class NumberOfContributors(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of Contributors",
            children,
            Impact.POSITIVE,
            "Contributors",
            "Calculating the number of contributors",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )