from datetime import datetime, timezone

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter

"""
augur measure. Avg Number of days issues have been open.
"""


class OpenIssueAgeVisitor(Visitor[float]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            date_now = datetime.now(timezone.utc)
            open_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state='open'
            )
            total_age_days = 0
            total_avg_age = 0
            for issue in open_issues:
                total_age_days += (date_now - issue.created_at).days
            if open_issues.totalCount > 0:
                total_avg_age = total_age_days / open_issues.totalCount
            print(f"{repository.full_name}: {measure.name} is {total_avg_age} {measure.unit}")
            return total_avg_age
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
