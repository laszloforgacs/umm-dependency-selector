from domain.model.Measure import BaseMeasure

"""
Time since the last commit measured in months.
"""
class TimeSinceLastCommit(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("TimeSinceLastCommit", "months", 1, visitor)
