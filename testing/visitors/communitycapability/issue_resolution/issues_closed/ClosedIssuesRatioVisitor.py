import os
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github import Github
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
CHAOSS metric attributed to Issue Resolution. Category 1 measure. Analysed in the last 3 months.
"""


class ClosedIssuesRatioVisitor(BaseMeasureVisitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            today = datetime.now(timezone.utc)
            start_date = today - relativedelta(months=3)

            total_issues = github_rate_limiter.execute(
                repository.get_issues,
                state="all"
            )
            total_issues_count = total_issues.totalCount

            closed_issues_in_period = github_rate_limiter.execute(
                repository.get_issues,
                since=start_date,
                state="closed"
            )

            closed_issues_in_period_count = closed_issues_in_period.totalCount

            if total_issues_count == 0:
                print(f"{repository.full_name}: {measure.name} is {closed_issues_in_period_count} {measure.unit}")
                return closed_issues_in_period_count

            ratio = closed_issues_in_period_count / total_issues_count

            print(f"{repository.full_name}: {measure.name} is {ratio} {measure.unit}")

            await self.cache_result(measure, repository, ratio)
            return ratio
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
