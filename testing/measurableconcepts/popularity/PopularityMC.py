from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class PopularityMC(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Popularity",
            children,
            Impact.POSITIVE,
            "repository properties",
            "Calculating the popularity of a repository",
            "Popularity affects 'Community and Adoption' positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
