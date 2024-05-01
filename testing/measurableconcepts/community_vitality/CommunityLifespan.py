from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect, Impact


class CommunityLifespan(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Community Lifespan",
            children,
            Impact.POSITIVE,
            "project repository",
            "Calculating the community lifespan in a repository",
            "Affects 'Community Vitality' positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor,
        )