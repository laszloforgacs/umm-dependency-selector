from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter


class DurationToResolveIssuesVisitor(Visitor[float]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            closed_issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state="closed"
            )
            time_differences = []
            for issue in closed_issues:
                time_differences.append(issue.closed_at - issue.created_at)

            if len(time_differences) == 0:
                # returning 90 days in seconds as an appropriately high value.
                upper_threshold = 90 * 24 * 60 * 60
                print(f"{repository.full_name}: {measure.name} is {upper_threshold}")
                return upper_threshold

            time_difference_seconds = [time_difference.total_seconds() for time_difference in time_differences]
            average_time_difference_seconds = sum(time_difference_seconds) / len(time_differences)
            average_time_difference_days = average_time_difference_seconds / (24 * 60 * 60)
            print(f"{repository.full_name}: {measure.name} is {average_time_difference_days} days")

            await self.cache_result(measure, repository, average_time_difference_days)
            return average_time_difference_days
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
