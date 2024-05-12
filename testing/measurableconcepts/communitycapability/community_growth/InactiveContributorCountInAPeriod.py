from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Community Growth. Category 1 measure
"""


class InactiveContributorCountInAPeriod(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Inactive Contributor Count In A Period",
            children,
            Impact.NEGATIVE,
            "contributors in issue tracker",
            "Calculating the number of contributors who have gone inactive in the analyzed period",
            "Developers going inactive affects community capability/product evolution negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
