from typing import Optional

from github.Repository import Repository

from presentation.core.visitors.Visitor import Visitor


class OSSAQMLicenseVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {repository.license}. Score: {score}")
                return cached_result

            if repository.license is None:
                print(f"{repository.full_name}: {measure.name} is None. Score: 1")
                return 1
            score = self._get_score(repository.license.key)
            print(f"{repository.full_name}: {measure.name} is {repository.license}. Score: {score}")
            await self.cache_result(measure, repository, score)
            return score

        except Exception as e:
            raise Exception(str(e))

    def _get_score(self, license_key: Optional[str]) -> int:
        scoring_table = {
            "none": 1,
            "other": 1,
            "gpl-2.0": 2,
            "lgpl-2.1": 2,
            "mpl-2.0": 3,
            "gpl-3.0": 3,
            "epl-2.0": 3,
            "agpl-3.0": 3,
            "cc0-1.0": 4,
            "bsl-1.0": 4,
            "bsd-2-clause": 4,
            "bsd-3-clause": 4,
            "unlicense": 4,
            "mit": 5,
            "apache-2.0": 5,
        }

        return scoring_table.get(license_key, 1)