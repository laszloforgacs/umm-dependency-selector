import os
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github import Github
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
CHAOSS workgroup's github page.
Counts the average number of contributors per pull request in the version control history.
The period will be the last 3 months for the sake of saving API limits.
"""


class AvgNumberOfContributorsPerPRsVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            contributors_count = 0
            start_date = datetime.now(timezone.utc) - relativedelta(months=3)
            pull_requests = github_rate_limiter.execute(
                repository.get_pulls,
                state="all",
                sort="created",
                direction="desc"
            )

            filtered_pull_requests = [pr for pr in pull_requests if pr.created_at >= start_date]

            for pr in filtered_pull_requests:
                contributors = set()
                contributors.add(
                    pr.user.login
                )
                commits = github_rate_limiter.execute(pr.get_commits)
                for commit in commits:
                    if commit.author is not None or commit.committer is not None:
                        contributors.add(
                            commit.author.login if commit.author else commit.committer.login
                        )
                contributors_count += len(contributors)

            if pull_requests.totalCount == 0:
                print(f"{repository.full_name}: {measure.name} is {0} {measure.unit}")
                return 0

            avg_contributors = contributors_count / pull_requests.totalCount

            print(f"{repository.full_name}: {measure.name} is {avg_contributors} {measure.unit}")

            await self.cache_result(measure, repository, avg_contributors)
            return avg_contributors
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
