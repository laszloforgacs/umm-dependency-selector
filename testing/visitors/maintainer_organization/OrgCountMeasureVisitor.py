import os

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
This class uses the implementation of criticality_score legacy python org_count signal.
"""


class OrgCountMeasureVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            self._init()

            orgs = set()
            contributors = self._github_rate_limiter.execute(
                repository.get_contributors
            )

            for contributor in contributors:
                if contributor.company is not None:
                    orgs.add(
                        self._filter_name(contributor.company)
                    )

            print(f"{repository.full_name}: {measure.name} is {len(orgs)} {measure.unit}")

            await self.cache_result(measure, repository, len(orgs))
            return len(orgs)
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _filter_name(self, org_name: str) -> str:
        return org_name.lower().replace('inc.', '').replace(
            'llc', '').replace('@', '').replace(' ', '').rstrip(',')

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
