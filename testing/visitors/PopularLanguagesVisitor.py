from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor

"""
Measure visitor implementation is taken from OSS-AQM
"""


class PopularLanguagesVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {repository.language}. Score: {cached_result}")
                return cached_result

            score = self._get_score(repository.language)

            print(f"{repository.full_name}: {measure.name} is {repository.language}. Score: {score}")

            await self.cache_result(measure, repository, score)
            return score
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _get_score(self, primary_language) -> int:
        languages = {
            'julia': 1, 'cobol': 1, 'pascal': 1, 'fortran': 1,
            'rust': 2, 'objective-c': 2, 'dart': 2, 'scala': 2,
            'perl': 2, 'haskell': 2, 'kotlin': 3, 'ruby': 3, 'assembly': 3,
            'vba': 3, 'swift': 3, 'r': 3, 'typescript': 4, 'php': 4, 'c#': 4,
            'c++': 4, 'c': 4, 'go': 4, 'javascript': 5, 'html': 5, 'css': 5,
            'python': 5, 'sql': 5, 'java': 5, 'shall': 5, 'bash': 5, 'powershell': 5
        }

        return languages.get(primary_language.lower(), 1)
