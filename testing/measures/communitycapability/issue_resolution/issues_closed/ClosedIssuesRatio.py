from domain.model.Measure import BaseMeasure, MeasurementMethod

"""
Belongs to Issue Resolution in CHAOSS. Category 1 measure
Closed issues in a specified period (3 months in this case) 
compared to the total number of issues that were created before the analysed period.
result = closed/total
"""


class ClosedIssuesRatio(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Closed Issues Ratio", "ratio", 1, MeasurementMethod.AUTOMATIC, visitor=visitor)
