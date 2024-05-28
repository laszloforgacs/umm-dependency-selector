import os

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token


class AugurClosedIssuesCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            self._github_rate_limiter = GithubRateLimiter(github=github)
            closed_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="closed"
            )
            print(f"{repository.full_name}: {measure.name} is {closed_issues.totalCount}")
            return closed_issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)