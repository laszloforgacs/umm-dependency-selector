from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
Sonar Maintainability Rating
"""


class MaintainabilityRating(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Rating given related to the amount of technical debt in the repository",
            children,
            Impact.NEGATIVE,
            "source code",
            "Calculating the maintainability rating of the repository",
            "High technical debt affects the maintainability of the software negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
