import os
from datetime import datetime, timezone

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
augur measure. Avg Number of days issues have been open.
"""


class OpenIssueAgeVisitor(Visitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            date_now = datetime.now(timezone.utc)
            open_issues = github_rate_limiter.execute(
                repository.get_issues,
                state='open'
            )
            total_age_days = 0
            total_avg_age = 0
            for issue in open_issues:
                total_age_days += (date_now - issue.created_at).days
            if open_issues.totalCount > 0:
                total_avg_age = total_age_days / open_issues.totalCount

            print(f"{repository.full_name}: {measure.name} is {total_avg_age} {measure.unit}")

            await self.cache_result(measure, repository, total_avg_age)
            return total_avg_age
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
