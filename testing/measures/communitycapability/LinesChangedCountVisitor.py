from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
CHAOSS workgroup's github page. Total number of line changes metric (during a period).
It is called Code Changes Lines.
Count. Total number of lines changes (touched) during the period.
As an example this will be 3 months
"""


class LinesChangedCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            total_changes = 0
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=3)
            commits = self._github_rate_limiter.execute(
                repository.get_commits,
                since=start_date,
                until=end_date
            )
            for commit in commits:
                total_changes += commit.stats.total

            print(f"{repository.full_name}: {measure.name} is {total_changes} {measure.unit}")
            return total_changes
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
