from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
From CHAOSS: Change Requests Duration
Category 1
"""


class ChangeRequestsDurationAverage(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Change Requests Duration",
            children,
            Impact.NEGATIVE,
            "pull requests in version control history",
            "The duration of time taken to accept or decline a pull request",
            "Longer time to resolve pull requests affects community capability or product evolution negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
