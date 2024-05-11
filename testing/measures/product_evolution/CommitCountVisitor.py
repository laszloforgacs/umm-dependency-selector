from datetime import datetime, timezone

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github.Repository import Repository

"""
criticality_score project, average commits per week in the last year
"""


class CommitCountVisitor(Visitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            end_date = datetime.now(timezone.utc)
            start_date = end_date.replace(year=end_date.year - 1)
            commits = repository.get_commits(since=start_date, until=end_date)
            weeks = 52

            commits_per_week = commits.totalCount / weeks
            print(f"{repository.full_name}: {measure.name} is {commits_per_week}")

            await self.cache_result(measure, repository, commits_per_week)
            return commits_per_week
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
