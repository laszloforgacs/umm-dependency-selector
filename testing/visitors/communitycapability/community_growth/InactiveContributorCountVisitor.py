import os
from datetime import timezone, datetime

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
from CHAOSS. belongs to Comunity Growth, Inactive Contributors
Category 1 measure
Analyzed in the last 1 year. We count the number of developers who went inactive in the last year.
The interval, or cutoff period is 180 days.
If a developer has not contributed in the last 180 days, they are considered inactive.
"""


class InactiveContributorCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        super().__init__()

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            self._init()

            contributors_going_inactive = 0
            # defining the start and end date
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(years=1)

            # defining the interval - how long it takes a contributor to be considered inactive
            interval_days = 180

            contributors = self._github_rate_limiter.execute(
                repository.get_contributors,
                anon='false'
            )

            for contributor in contributors:
                user_commits = self._github_rate_limiter.execute(
                    repository.get_commits,
                    author=contributor.login
                )

                if user_commits.totalCount > 0:
                    last_commit_date = user_commits[0].commit.author.date
                    is_between_end_and_start_date = start_date <= last_commit_date <= end_date
                    if not is_between_end_and_start_date:
                        continue

                    is_inactive = (end_date - last_commit_date).days > interval_days
                    if is_inactive:
                        contributors_going_inactive += 1

            print(
                f"{repository.full_name}: Number of inactive contributors between {start_date.date()} and {end_date.date()}: {contributors_going_inactive}")

            await self.cache_result(measure, repository, contributors_going_inactive)
            return contributors_going_inactive
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
