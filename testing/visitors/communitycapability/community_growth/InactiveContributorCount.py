from domain.model.Measure import MeasurementMethod, BaseMeasure

"""
from CHAOSS. belongs to Comunity Growth, Inactive Contributors
Category 1 measure
Analyzed in the last 1 year. We count the number of developers who went inactive in the last year.
The interval, or cutoff period is 180 days.
If a developer has not contributed in the last 180 days, they are considered inactive.
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
