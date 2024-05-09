from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Issue Resolution. Category 1 measure
"""


class IssuesClosedCount(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Issues Closed Count",
            children,
            Impact.POSITIVE,
            "issues in version control history",
            "Calculating the number of closed issues in the version control history",
            "Closing issues signal community activity and affect product evolution/community capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
