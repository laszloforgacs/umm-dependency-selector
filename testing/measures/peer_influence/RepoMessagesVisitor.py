from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor, T
from util.GithubRateLimiter import GithubRateLimiter

"""
Augur measure: Number of messages exchanged for a repository over a specified period.
(In the last 3 months)
"""


class RepoMessagesVisitor(BaseMeasureVisitor[int]):

    def __init__(self, github_rate_limiter: GithubRateLimiter):
        super().__init__()
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=3)
            total_comments = 0
            pr_comments = self._github_rate_limiter.execute(
                repository.get_pulls_comments,
                sort='updated',
                direction='desc',
                since=start_date
            )
            total_comments += pr_comments.totalCount
            print(f"{repository.full_name}: {measure.name} is {total_comments}")
            return total_comments
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
