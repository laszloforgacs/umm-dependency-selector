import os

from github import Github

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Comes from augur. Average time to respond to an issue in a repository.
Also a CHAOSS measure.
CATEGORY 1
"""


class IssueResponseTimeVisitor(Visitor[float]):
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

            issues = github_rate_limiter.execute(
                repository.get_issues,
                state="all"
            )
            time_differences = []
            for issue in issues:
                comments = github_rate_limiter.execute(
                    issue.get_comments
                )
                if comments.totalCount > 0:
                    first_comment = comments[0]

                    if first_comment and issue.created_at:
                        time_difference = first_comment.created_at - issue.created_at
                        time_differences.append(time_difference)

            if not time_differences:
                # returning 30 days in seconds as an appropriately high value.
                upper_threshold = 30 * 24 * 60 * 60
                print(f"{repository.full_name}: {measure.name} is {upper_threshold}")
                return upper_threshold
            else:
                total_time_difference_seconds = sum(
                    [time_difference.total_seconds() for time_difference in time_differences])
                average_time_difference_seconds = total_time_difference_seconds / len(time_differences)
                print(f"{repository.full_name}: {measure.name} is {average_time_difference_seconds}")

                await self.cache_result(measure, repository, average_time_difference_seconds)
                return average_time_difference_seconds
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
