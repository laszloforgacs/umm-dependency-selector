import os
from datetime import timezone, datetime

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github import Github
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
from CHAOSS. belongs to Comunity Growth, Number of Downloads
"""


class AssetDownloadCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        super().__init__()

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            self._init()

            count = 0
            releases = self._github_rate_limiter.execute(repository.get_releases)
            for release in releases:
                assets = self._github_rate_limiter.execute(release.get_assets)
                for asset in assets:
                    count += asset.download_count

            print(f"Asset download count: {count}")

            await self.cache_result(measure, repository, count)
            return count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
