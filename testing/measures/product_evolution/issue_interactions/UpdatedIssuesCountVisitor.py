from datetime import datetime, timezone, timedelta

from presentation.core.visitors.Visitor import Visitor


"""
criticality_score measure: Number of issues updated in the last 90 days.
Indicates high contributor involvement.
Lower weight since it is dependent on project contributors.
"""
class UpdatedIssuesCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=90)
            updated_issues = repository.get_issues(sort='updated', since=start_date)
            total_count = 1
            total_count += updated_issues.totalCount
            print(f"{repository.full_name}: {measure.name} is {total_count}")
            return total_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)