import os
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github import Github
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
CHAOSS workgroup's github page. Total number of line changes metric (during a period).
It is called Code Changes Lines.
Count. Total number of lines changes (touched) during the period.
As an example this will be 3 months
"""


class LinesChangedCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            total_changes = 0
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=3)
            commits = github_rate_limiter.execute(
                repository.get_commits,
                since=start_date,
                until=end_date
            )
            for commit in commits:
                total_changes += commit.stats.total

            print(f"{repository.full_name}: {measure.name} is {total_changes} {measure.unit}")

            await self.cache_result(measure, repository, total_changes)
            return total_changes
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
