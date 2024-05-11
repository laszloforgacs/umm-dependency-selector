from domain.model.Measure import BaseMeasure, MeasurementMethod

"""
Belongs to ClosedIssuesCountByNewContributors, Community Growth, New Contributors Closing Issues
It just a measure that helps to gather the new contributors in a list, which is passed to the
derived measure ClosedIssuesCountByNewContributors.
"""


class NewContributors(BaseMeasure[list[str]]):
    def __init__(
            self,
            visitor=None
    ):
        super().__init__(
            "New Contributors list",
            "contributor(s)",
            1.0,
            MeasurementMethod.AUTOMATIC,
            visitor
        )
