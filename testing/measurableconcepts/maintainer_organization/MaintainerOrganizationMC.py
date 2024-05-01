from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class MaintainerOrganizationMC(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Maintainer Organization",
            children,
            Impact.POSITIVE,
            "contributor list",
            "Calculation of the number of maintianer organizations",
            "Affects 'Community and Adoption' positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
