import os

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token


class AvgTimeToFixBugsVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        self._github_rate_limiter = None

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result} {measure.unit}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            self._github_rate_limiter = GithubRateLimiter(github=github)

            bug_labels = self._get_bug_labels(repository)
            bugs = repository.get_issues(labels=bug_labels, state='closed')
            time_differences = []
            for bug in bugs:
                time_differences.append(bug.closed_at - bug.created_at)

            if len(time_differences) == 0:
                upper_threshold = 90 * 24 * 60 * 60
                print(f"{repository.full_name}: {measure.name} is {upper_threshold}")
                return upper_threshold

            time_difference_seconds = [time_difference.total_seconds() for time_difference in time_differences]
            average_time_difference_seconds = sum(time_difference_seconds) / len(time_differences)
            average_time_difference_days = average_time_difference_seconds / (24 * 60 * 60)

            print(f"{repository.full_name}: {measure.name} is {average_time_difference_days} {measure.unit}")

            await self.cache_result(measure, repository, average_time_difference_days)
            return average_time_difference_days
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _get_bug_labels(self, repository: 'Repository') -> list[str]:
        try:
            labels = self._github_rate_limiter.execute(
                repository.get_labels
            )
            bug_labels = [label.name for label in labels if 'bug' in label.name.lower()]
            return bug_labels
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
