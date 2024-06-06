import os
from datetime import timezone, datetime

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Augur measure that counts the number of opened pull request in a period of time.
It's 6 months by default.
"""


class OpenedPullRequestCountVisitor(Visitor[int]):
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

            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=6)
            opened_pull_requests = github_rate_limiter.execute(
                repository.get_pulls,
                sort='created',
                direction='desc'
            )
            opened_pull_request_count = 0
            for pull_request in opened_pull_requests:
                if start_date <= pull_request.created_at <= end_date:
                    opened_pull_request_count += 1
                else:
                    break

            print(f"{repository.full_name}: {measure.name} is {opened_pull_request_count}")

            await self.cache_result(measure, repository, opened_pull_request_count)
            return opened_pull_request_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
