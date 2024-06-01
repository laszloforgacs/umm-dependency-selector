from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
CHAOSS workgroup's github page. Part of Change Request Commits measurable concept.
Counts the average number of commits per pull request in the version control history.
The period will be the last 3 months for the sake of saving API limits.
"""


class AvgNumberOfCommitsPerPRsVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            default_upper_threshold = 50
            total_commits = 0
            start_date = datetime.now(timezone.utc) - relativedelta(months=3)
            pull_requests = self._github_rate_limiter.execute(
                repository.get_pulls,
                state="all",
                sort="created",
                direction="desc"
            )

            filtered_pull_requests = [pr for pr in pull_requests if pr.created_at >= start_date]

            for pr in filtered_pull_requests:
                commits = self._github_rate_limiter.execute(pr.get_commits)
                total_commits += commits.totalCount

            if pull_requests.totalCount == 0:
                print(f"{repository.full_name}: {measure.name} is {default_upper_threshold} {measure.unit}")
                return default_upper_threshold

            avg_commits = total_commits / pull_requests.totalCount

            print(f"{repository.full_name}: {measure.name} is {avg_commits} {measure.unit}")

            await self.cache_result(measure, repository, avg_commits)
            return avg_commits
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
