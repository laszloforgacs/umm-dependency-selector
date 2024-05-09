from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
from CHAOSS. New Contributors
Category 1
Belongs to Community Growth on CHAOSS
"""


class NewContributorsMC(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of New Contributors",
            children,
            Impact.POSITIVE,
            "project contributors",
            "Calculating the new contributors to the project",
            "Affects 'Community Exists' positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
