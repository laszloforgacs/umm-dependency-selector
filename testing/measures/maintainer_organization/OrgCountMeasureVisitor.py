from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter

"""
This class uses the implementation of criticality_score legacy python org_count signal.
"""


class OrgCountMeasureVisitor(BaseMeasureVisitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
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
            return len(orgs)
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _filter_name(self, org_name: str) -> str:
        return org_name.lower().replace('inc.', '').replace(
            'llc', '').replace('@', '').replace(' ', '').rstrip(',')
