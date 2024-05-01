from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter


class AugurClosedIssuesCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            closed_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="closed"
            )
            print(f"{repository.full_name}: {measure.name} is {closed_issues.totalCount}")
            return closed_issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)