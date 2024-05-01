from datetime import datetime, timezone

from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor, T
from util.GithubRateLimiter import GithubRateLimiter


class RepositoryAgeMeasureVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self.github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            today = datetime.now(timezone.utc)
            created_at = repository.created_at
            age = today - created_at
            years = age.days // 365
            print(f"{repository.full_name}: {measure.name} is {years} {measure.unit}")
            return years
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)


