from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class CommunityInteractionMC(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Community Interaction",
            children,
            Impact.POSITIVE,
            "project contributors",
            "Calculating the community interaction of the project",
            "Affects 'Community Exists' positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )