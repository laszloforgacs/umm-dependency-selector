from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
CHAOSS metric attributed to Issue Resolution. Category 1 measure. Analysed in the last 3 months.
"""


class ActiveIssuesRatioVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            today = datetime.now(timezone.utc)
            start_date = today - relativedelta(months=3)

            total_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="all"
            )
            total_issues_count = total_issues.totalCount

            updated_issues_in_period = self._github_rate_limiter.execute(
                repository.get_issues,
                since=start_date,
                state="all"
            )
            updated_issues_in_period_count = updated_issues_in_period.totalCount

            if total_issues_count == 0:
                print(f"{repository.full_name}: {measure.name} is {updated_issues_in_period_count} {measure.unit}")
                return updated_issues_in_period_count

            ratio = updated_issues_in_period_count / total_issues_count

            print(f"{repository.full_name}: {measure.name} is {ratio} {measure.unit}")

            await self.cache_result(measure, repository, ratio)
            return ratio
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
