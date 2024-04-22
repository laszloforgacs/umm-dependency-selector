from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter

"""
Augur measure: Time series of number of accepted reviews / pull requests opened within a certain period
"""


class ReviewsAcceptedRatioVisitor(Visitor[float]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=6)
            pull_requests = self._github_rate_limiter.execute(
                repository.get_pulls,
                state='closed',
                direction='desc'
            )

            pull_requests_within_date = [pull_request for pull_request in pull_requests if
                                         start_date <= pull_request.created_at <= end_date]
            accepted_count = sum(1 for pull_request in pull_requests_within_date if pull_request.merged_at is not None)

            opened_pull_requests = self._github_rate_limiter.execute(
                repository.get_pulls,
                direction='desc'
            )
            opened_pull_requests_within_date = [pull_request for pull_request in opened_pull_requests if
                                               start_date <= pull_request.created_at <= end_date]
            total_opened_pull_requests = 0
            for _ in opened_pull_requests_within_date:
                total_opened_pull_requests += 1

            if total_opened_pull_requests == 0:
                print(f"{repository.full_name}: {measure.name} is {accepted_count}")
                return accepted_count

            ratio = accepted_count / total_opened_pull_requests
            print(f"{repository.full_name}: {measure.name} is {ratio}")
            return ratio
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
