from domain.model.Measure import BaseMeasure, MeasurementMethod

"""
Belongs to Issue Resolution in CHAOSS. Category 1 measure
Issues updated in a specified period (3 months in this case) 
compared to the total number of issues that were created before the analysed period.
result = updated/total
"""


class ActiveIssuesRatio(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Active Issues Ratio", "ratio", 1, MeasurementMethod.AUTOMATIC, visitor=visitor)
