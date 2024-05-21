from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect

"""
Category 2 provided by Sonar.
"""


class DuplicatedBlocks(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Duplicated Blocks",
            children,
            Impact.NEGATIVE,
            "source code",
            "Measuring the number of duplicated blocks in the source code",
            "Affects reusability negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
