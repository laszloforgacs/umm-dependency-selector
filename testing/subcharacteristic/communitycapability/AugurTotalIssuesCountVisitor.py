import os

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token


class AugurTotalIssuesCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            self._github_rate_limiter = GithubRateLimiter(github=github)
            issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="all"
            )
            print(f"{repository.full_name}: {measure.name} is {issues.totalCount}")
            return issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)