import os

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
CHAOSS metric attributed to Change Request Reviews measurable concept.
"""


class PercentageOfPRsReviewedVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            human_reviewed_prs = 0
            closed_prs = github_rate_limiter.execute(
                repository.get_pulls,
                state="closed"
            )

            if closed_prs.totalCount == 0:
                print(f"{repository.full_name}: {measure.name} is {0} {measure.unit}")
                return 0

            for pr in closed_prs:
                reviews = github_rate_limiter.execute(pr.get_reviews)
                is_human_reviewed = any(
                    review.user is not None and review.user.type == "User" for review in reviews
                )
                if is_human_reviewed:
                    human_reviewed_prs += 1

            percentage = human_reviewed_prs / closed_prs.totalCount * 100

            print(f"{repository.full_name}: {measure.name} is {percentage}{measure.unit}")

            await self.cache_result(measure, repository, percentage)
            return percentage
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
