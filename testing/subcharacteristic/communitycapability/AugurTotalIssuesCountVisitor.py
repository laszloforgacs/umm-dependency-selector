from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter


class AugurTotalIssuesCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="all"
            )
            print(f"{repository.full_name}: {measure.name} is {issues.totalCount}")

            await self.cache_result(measure, repository, issues.totalCount)
            return issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)