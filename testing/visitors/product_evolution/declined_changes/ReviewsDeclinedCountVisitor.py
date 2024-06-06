import os

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token


class ReviewsDeclinedCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            closed_issues = github_rate_limiter.execute(
                repository.get_pulls,
                state='closed'
            )
            declined_count = sum(1 for issue in closed_issues if issue.merged_at is None)
            print(f"{repository.full_name}: {measure.name} is {declined_count}")

            await self.cache_result(measure, repository, declined_count)
            return declined_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
