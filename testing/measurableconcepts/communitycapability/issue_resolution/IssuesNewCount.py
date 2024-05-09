from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Issue Resolution. Category 1 measure
"""


class IssuesNewCount(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Issues New Count",
            children,
            Impact.POSITIVE,
            "issues in version control history",
            "Calculating the number of new issues in the version control history",
            "New issues are a proxy for activity and affect product evolution/community capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
