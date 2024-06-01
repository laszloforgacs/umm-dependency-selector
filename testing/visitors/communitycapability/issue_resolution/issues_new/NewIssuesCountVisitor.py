from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
CHAOSS metric attributed to Issue Resolution. Category 1 measure. Analysed in the last 3 months.
"""


class NewIssuesCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            start_date = datetime.now(timezone.utc) - relativedelta(months=3)
            issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="all",
                sort="created",
                direction="desc"
            )

            new_issues = []
            for issue in issues:
                if issue.created_at >= start_date:
                    new_issues.append(issue)
                else:
                    break

            new_issues_count = len(new_issues)

            print(f"{repository.full_name}: {measure.name} is {new_issues_count} {measure.unit}")

            await self.cache_result(measure, repository, new_issues_count)
            return new_issues_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
