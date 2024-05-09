from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
CHAOSS metric attributed to Issue Resolution. Category 1 measure. Analysed in the last 3 months.
"""


class ActiveIssuesCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            start_date = datetime.now(timezone.utc) - relativedelta(months=3)
            issues = self._github_rate_limiter.execute(
                repository.get_issues,
                since=start_date
            )

            print(f"{repository.full_name}: {measure.name} is {issues.totalCount} {measure.unit}")
            return issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
