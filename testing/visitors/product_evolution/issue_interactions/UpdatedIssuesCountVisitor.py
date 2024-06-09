import os
from datetime import datetime, timezone, timedelta

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

from github import Github
from github.Repository import Repository

"""
criticality_score measure: Number of issues updated in the last 90 days.
Indicates high contributor involvement.
Lower weight since it is dependent on project contributors.
"""


class UpdatedIssuesCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            self._init()

            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=90)
            updated_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                since=start_date,
                state="all"
            )
            print(f"{repository.full_name}: {measure.name} is {updated_issues.totalCount}")

            await self.cache_result(measure, repository, updated_issues.totalCount)
            return updated_issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
