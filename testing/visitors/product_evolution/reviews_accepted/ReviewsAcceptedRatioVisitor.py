import os
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github import Github

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Augur measure: Time series of number of accepted reviews / pull requests opened within a certain period
"""


class ReviewsAcceptedRatioVisitor(Visitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=6)
            pull_requests = github_rate_limiter.execute(
                repository.get_pulls,
                state='closed',
                direction='desc'
            )

            pull_requests_within_date = [pull_request for pull_request in pull_requests if
                                         start_date <= pull_request.created_at <= end_date]
            accepted_count = sum(1 for pull_request in pull_requests_within_date if pull_request.merged_at is not None)

            opened_pull_requests = github_rate_limiter.execute(
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

            await self.cache_result(measure, repository, ratio)
            return ratio
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
