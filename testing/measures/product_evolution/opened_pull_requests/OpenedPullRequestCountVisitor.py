from datetime import timezone, datetime

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter

"""
Augur measure that counts the number of opened pull request in a period of time.
It's 6 months by default.
"""


class OpenedPullRequestCountVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date.replace(month=end_date.month - 6)
            opened_pull_requests = self._github_rate_limiter.execute(
                repository.get_pulls,
                sort='created',
                direction='desc'
            )
            opened_pull_request_count = 0
            for pull_request in opened_pull_requests:
                if start_date <= pull_request.created_at <= end_date:
                    opened_pull_requests += 1
                else:
                    break
            print(f"{repository.full_name}: {measure.name} is {opened_pull_request_count}")
            return opened_pull_request_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
