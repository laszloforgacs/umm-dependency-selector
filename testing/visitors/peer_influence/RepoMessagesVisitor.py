import os
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github import Github
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor, T
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Augur measure: Number of messages exchanged for a repository over a specified period.
(In the last 3 months)
"""


class RepoMessagesVisitor(BaseMeasureVisitor[int]):

    def __init__(self):
        super().__init__()

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            self._init()

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

            await self.cache_result(measure, repository, total_comments)
            return total_comments
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
