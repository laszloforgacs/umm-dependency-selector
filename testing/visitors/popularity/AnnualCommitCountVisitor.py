import os
from datetime import datetime, timezone

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Measured in Augur. Called Annual Commit Count.
"""


class AnnualCommitCountVisitor(BaseMeasureVisitor[int]):
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

            end_date = datetime.now(timezone.utc)
            start_date = end_date.replace(year=end_date.year - 1)

            commits = github_rate_limiter.execute(
                repository.get_commits,
                since=start_date,
                until=end_date
            )
            print(f"{repository.full_name}: {measure.name} is {commits.totalCount}")

            await self.cache_result(measure, repository, commits.totalCount)
            return commits.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
