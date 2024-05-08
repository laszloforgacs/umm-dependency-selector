from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measure called Change Request Reviews
CATEGORY 1
"""


class ChangeRequestReviews(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Change Request Reviews",
            children,
            Impact.POSITIVE,
            "pull requests in version control history",
            "Calculating the percentage of closed pull requests that have been reviewed",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
