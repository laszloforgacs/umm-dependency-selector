from datetime import datetime, timezone

from presentation.core.visitors.Visitor import Visitor

"""
augur measure. Number of days an issue has been open.
"""
class OpenIssueAgeVisitor(Visitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            date_now = datetime.now(timezone.utc)
            open_issues = repository.get_issues(state='open')
            total_age = 1
            for issue in open_issues:
                total_age += date_now - issue.created_at.days
            if open_issues.totalCount > 0:
                total_age = total_age / open_issues.totalCount
            print(f"{repository.full_name}: {measure.name} is {total_age}")
            return total_age
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)