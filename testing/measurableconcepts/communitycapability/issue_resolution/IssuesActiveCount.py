from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Issue Resolution. Category 1 measure
"""


class IssuesActiveCount(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Issues Active Count",
            children,
            Impact.POSITIVE,
            "issues in version control history",
            "Calculating the number of active issues in the version control history",
            "Active issues signal community activity and affect product evolution/community capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
