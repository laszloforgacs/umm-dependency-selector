from domain.model.Measure import BaseMeasure

"""
CHAOSS Issue Response Time CATEGORY 1
"""


class IssueResponseTime(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Issue Response Time", "issue", 1, visitor=visitor)
