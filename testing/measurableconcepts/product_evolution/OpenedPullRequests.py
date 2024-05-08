from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


"""
Augur: Pull Requests News
CHAOSS: Change Requests (count)
Category 1
"""
class OpenedPullRequests(MeasurableConcept[int]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Opened pull requests in a period",
            children,
            Impact.POSITIVE,
            "version control history",
            "Calculating the number of opened pull requests",
            "Pull requests affect product evolution positively, and are a proxy for activity",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )