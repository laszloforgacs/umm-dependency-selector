import os

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token


class PyGithubCommunityCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            self._github_rate_limiter = GithubRateLimiter(github=github)
            contributors = self._github_rate_limiter.execute(repository.get_contributors)
            contributors_count = sum(1 for _ in contributors)
            print(f"{repository.full_name}: {measure.name} is {contributors_count}")
            return contributors_count
        except Exception as e:
            raise Exception(str(e))