import os

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token


class NumberOfBugsToFixVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        self._github_rate_limiter = None

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            self._github_rate_limiter = GithubRateLimiter(github=github)

            bug_labels = self._get_bug_labels(repository)
            open_bugs = self._github_rate_limiter.execute(
                repository.get_issues,
                labels=bug_labels,
                state='open'
            )
            print(f"{repository.full_name}: {measure.name} is {open_bugs.totalCount}")

            await self.cache_result(measure, repository, open_bugs.totalCount)
            return open_bugs.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _get_bug_labels(self, repository: 'Repository') -> list[str]:
        try:
            labels = self._github_rate_limiter.execute(
                repository.get_labels
            )
            bug_labels = [label.name for label in labels if 'bug' in label.name.lower()]
            return bug_labels
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
