from datetime import datetime, timezone, timedelta

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter

"""
criticality_score measure: Number of issues updated in the last 90 days.
Indicates high contributor involvement.
Lower weight since it is dependent on project contributors.
"""


class UpdatedIssuesCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=90)
            updated_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                since=start_date,
                state="all"
            )
            print(f"{repository.full_name}: {measure.name} is {updated_issues.totalCount}")
            return updated_issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
