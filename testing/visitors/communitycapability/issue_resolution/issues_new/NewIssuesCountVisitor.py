import os
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github import Github
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
CHAOSS metric attributed to Issue Resolution. Category 1 measure. Analysed in the last 3 months.
"""


class NewIssuesCountVisitor(BaseMeasureVisitor[int]):
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

            start_date = datetime.now(timezone.utc) - relativedelta(months=3)
            issues = github_rate_limiter.execute(
                repository.get_issues,
                state="all",
                sort="created",
                direction="desc"
            )

            new_issues = []
            for issue in issues:
                if issue.created_at >= start_date:
                    new_issues.append(issue)
                else:
                    break

            new_issues_count = len(new_issues)

            print(f"{repository.full_name}: {measure.name} is {new_issues_count} {measure.unit}")

            await self.cache_result(measure, repository, new_issues_count)
            return new_issues_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
