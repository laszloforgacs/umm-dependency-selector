from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter


class DurationToResolveIssuesVisitor(Visitor[float]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            return 49.0
            closed_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="closed"
            )
            time_differences = []
            for issue in closed_issues:
                time_differences.append(issue.closed_at - issue.created_at)

            if len(time_differences) == 0:
                # returning 90 days in seconds as an appropriately high value.
                print(f"{repository.full_name}: {measure.name} is {90 * 24 * 60 * 60}")
                return 90 * 24 * 60 * 60

            time_difference_seconds = [time_difference.total_seconds() for time_difference in time_differences]
            average_time_difference_seconds = sum(time_difference_seconds) / len(time_differences)
            print(f"{repository.full_name}: {measure.name} is {average_time_difference_seconds}")
            return average_time_difference_seconds
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)