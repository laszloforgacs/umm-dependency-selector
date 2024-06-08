import os

from github import Github
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Measured in Augur. Called Watchers Count.
"""


class WatchersCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            self._init()

            watchers = self._github_rate_limiter.execute(
                repository.get_watchers
            )

            print(f"{repository.full_name}: {measure.name} is {watchers.totalCount}")

            await self.cache_result(measure, repository, watchers.totalCount)
            return watchers.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
