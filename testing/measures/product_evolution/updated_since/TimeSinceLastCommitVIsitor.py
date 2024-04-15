from datetime import datetime, timezone

from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github.Repository import Repository


class TimeSinceLastCommitVisitor(Visitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        try:
            # default time threshold is 1 year in months
            default_time_threshold = 12
            current_date = datetime.now(timezone.utc)

            commits = repository.get_commits()
            if commits.totalCount == 0:
                print(f"{repository.full_name}: {measure.name} is {default_time_threshold}")
                return default_time_threshold

            last_commit = commits[0]
            last_commit_date = last_commit.commit.author.date
            time_since_last_commit = current_date - last_commit_date
            return time_since_last_commit.days / 30
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)