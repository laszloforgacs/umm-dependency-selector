from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
CHAOSS metric attributed to Change Request Reviews measurable concept.
"""


class PercentageOfPRsReviewedVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        super().__init__()
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            human_reviewed_prs = 0
            closed_prs = self._github_rate_limiter.execute(
                repository.get_pulls,
                state="closed"
            )

            if closed_prs.totalCount == 0:
                print(f"{repository.full_name}: {measure.name} is {0} {measure.unit}")
                return 0

            for pr in closed_prs:
                reviews = self._github_rate_limiter.execute(pr.get_reviews)
                is_human_reviewed = any(review.user.type == "User" for review in reviews)
                if is_human_reviewed:
                    human_reviewed_prs += 1

            percentage = human_reviewed_prs / closed_prs.totalCount * 100
            print(f"{repository.full_name}: {measure.name} is {percentage}{measure.unit}")
            return percentage
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
