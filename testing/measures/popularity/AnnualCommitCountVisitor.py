from datetime import datetime, timezone

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
Measured in Augur. Called Annual Commit Count.
"""


class AnnualCommitCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date.replace(year=end_date.year - 1)
            commits = repository.get_commits(since=start_date, until=end_date)
            print(f"{repository.full_name}: {measure.name} is {commits.totalCount}")
            return commits.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
