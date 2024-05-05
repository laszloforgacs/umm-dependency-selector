from datetime import datetime, timezone

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
Measured in Augur. Called Number of Downloads on the workgroup's page.
"""


class DownloadsCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            downloads = self._github_rate_limiter.execute(
                repository.get_downloads
            )
            print(f"{repository.full_name}: {measure.name} is {downloads.totalCount}")
            return downloads.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
