import asyncio

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter
from util.Sonar import Sonar

"""
Sonar measure - Reliability Rating
"""


class LevelOfReliabilityVisitor(BaseMeasureVisitor[float]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        try:
            sonar = Sonar(
                quality_model_name=measure.get_quality_model().name,
                viewpoint_name=measure.get_viewpoint().name,
                repository=repository
            )

            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                converted_reliability_rating = self._convert_reliability_rating(cached_result)
                print(
                    f"{repository.full_name}: {measure.name} is {converted_reliability_rating}, rating {self._get_literal_rating(converted_reliability_rating)}")
                return converted_reliability_rating

            sonar_cache = await sonar.get_cached_result()
            if sonar_cache is not None:
                reliability_rating = float(sonar_cache.get("reliability_rating", 5.0))
                converted_reliability_rating = self._convert_reliability_rating(reliability_rating)
                print(
                    f"{repository.full_name}: {measure.name} is {converted_reliability_rating}, rating {self._get_literal_rating(converted_reliability_rating)}")
                await self.cache_result(measure, repository, reliability_rating)
                return converted_reliability_rating

            result = await asyncio.create_task(
                sonar.measure()
            )

            reliability_rating = float(result.get("reliability_rating", 5.0))
            converted_reliability_rating = self._convert_reliability_rating(reliability_rating)
            print(
                f"{repository.full_name}: {measure.name} is {converted_reliability_rating}, rating {self._get_literal_rating(converted_reliability_rating)}")
            await self.cache_result(measure, repository, reliability_rating)
            return converted_reliability_rating
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _convert_reliability_rating(self, sonar_reliability_rating: float) -> float:
        # Sonar reliability rating is 1-5, where 1 is the best and 5 is the worst
        if sonar_reliability_rating == 1.0:
            return 5.0
        elif sonar_reliability_rating == 2.0:
            return 4.0
        elif sonar_reliability_rating == 3.0:
            return 3.0
        elif sonar_reliability_rating == 4.0:
            return 2.0
        elif sonar_reliability_rating == 5.0:
            return 1.0
        else:
            return 1.0

    def _get_literal_rating(self, converted_rating: float) -> float:
        if converted_rating == 5.0:
            return "A"
        elif converted_rating == 4.0:
            return "B"
        elif converted_rating == 3.0:
            return "C"
        elif converted_rating == 2.0:
            return "D"
        elif converted_rating == 1.0:
            return "E"
        else:
            return "E"
