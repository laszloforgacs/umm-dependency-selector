from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Issue Resolution. Category 1 measure
"""


class IssuesActiveRatio(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Issues Active Ratio",
            children,
            Impact.POSITIVE,
            "issues in version control history",
            "Calculating the ratio of active issues to the total number of issues in the version control history",
            "Active issues signal community activity and affect product evolution/community capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
