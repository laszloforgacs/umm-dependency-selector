from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter

"""
CHAOSS metric: The number of accepted pull requests.
"""


class ReviewsAcceptedCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            closed_issues = self._github_rate_limiter.execute(
                repository.get_pulls,
                state='closed'
            )

            accepted_count = sum(1 for issue in closed_issues if issue.merged_at is not None)

            print(f"{repository.full_name}: {measure.name} is {accepted_count}")

            await self.cache_result(measure, repository, accepted_count)
            return accepted_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
