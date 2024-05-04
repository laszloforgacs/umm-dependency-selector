from datetime import datetime, timezone

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
Measured in Augur. Called Forks Count.
"""


class ForksCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            print(f"{repository.full_name}: {measure.name} is {repository.forks_count}")
            return repository.forks_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
