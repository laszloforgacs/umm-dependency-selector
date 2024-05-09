from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter

"""
Comes from augur. Average time to respond to an issue in a repository.
"""


class IssueResponseTimeVisitor(Visitor[float]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            return 169.0
            issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="all"
            )
            time_differences = []
            for issue in issues:
                comments = self._github_rate_limiter.execute(
                    issue.get_comments
                )
                if comments.totalCount > 0:
                    first_comment = comments[0]

                    if first_comment and issue.created_at:
                        time_difference = first_comment.created_at - issue.created_at
                        time_differences.append(time_difference)

            if not time_differences:
                # returning 30 days in seconds as an appropriately high value.
                print(f"{repository.full_name}: {measure.name} is {30 * 24 * 60 * 60}")
                return 30 * 24 * 60 * 60
            else:
                total_time_difference_seconds = sum(
                    [time_difference.total_seconds() for time_difference in time_differences])
                average_time_difference_seconds = total_time_difference_seconds / len(time_differences)
                print(f"{repository.full_name}: {measure.name} is {average_time_difference_seconds}")
                return average_time_difference_seconds
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
