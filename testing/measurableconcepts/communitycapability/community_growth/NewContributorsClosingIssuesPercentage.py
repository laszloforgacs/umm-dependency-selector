from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Community Growth. Category 1 measure
"""


class NewContributorsClosingIssuesPercentage(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "New Contributors Closing Issues Percentage",
            children,
            Impact.POSITIVE,
            "issues in the issue tracker",
            "Calculating the percentage of new contributors closing issues in the issue tracker compared to the total number of issues closed by new contributors in the analyzed period",
            "New contributors closing issues signal community growth and affect product evolution/community capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
