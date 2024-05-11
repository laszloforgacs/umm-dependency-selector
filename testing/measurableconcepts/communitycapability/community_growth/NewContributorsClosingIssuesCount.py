from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Community Growth. Category 1 measure
"""


class NewContributorsClosingIssuesCount(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "New Contributors Closing Issues Count",
            children,
            Impact.POSITIVE,
            "issues in the issue tracker",
            "Calculating the number of new contributors closing issues in the issue tracker",
            "New contributors closing issues signal community growth and affect product evolution/community capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
