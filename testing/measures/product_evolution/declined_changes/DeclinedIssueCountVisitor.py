from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter


class DeclinedIssueCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self.__github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            closed_issues = self.__github_rate_limiter.execute(
                repository.get_pulls,
                state='closed'
            )
            declined_count = sum(1 for issue in closed_issues if issue.merged_at is not None)
            print(f"{repository.full_name}: {measure.name} is {declined_count}")
            return declined_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
