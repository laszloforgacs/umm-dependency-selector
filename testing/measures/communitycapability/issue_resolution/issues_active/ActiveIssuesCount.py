from domain.model.Measure import BaseMeasure, MeasurementMethod

"""
Belongs to Issue Resolution in CHAOSS. Category 1 measure
"""


class ActiveIssuesCount(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Active Issues Count", "issue(s)", 1, MeasurementMethod.AUTOMATIC, visitor=visitor)
