from domain.model.Measure import MeasurementMethod, BaseMeasure

"""
from CHAOSS. belongs to Comunity Growth, Inactive Contributors
Category 1 measure
Analyzed in the last 3 months, which means we list the developers who went inactive in the last 3 months, but were active before that period.
"""


class InactiveContributorCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__(
            "Number of inactive contributors",
            "contributor(s)",
            1.0,
            MeasurementMethod.AUTOMATIC,
            visitor
        )
