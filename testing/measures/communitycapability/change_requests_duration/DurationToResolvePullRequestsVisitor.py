from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.GithubRateLimiter import GithubRateLimiter


class DurationToResolvePullRequestsVisitor(BaseMeasureVisitor[float]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            closed_prs = self._github_rate_limiter.execute(
                repository.get_pulls,
                state="closed"
            )
            time_differences = []
            for pr in closed_prs:
                time_differences.append(pr.closed_at - pr.created_at)

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
