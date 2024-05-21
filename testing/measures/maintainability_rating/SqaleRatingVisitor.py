import asyncio
import json

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter
from util.Sonar import Sonar

"""
Sonar measure
"""


class SqaleRatingVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
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
                print(f"{repository.full_name}: {measure.name} is {cached_result} {measure.unit}")
                return cached_result

            sonar_cache = await sonar.get_cached_result()
            if sonar_cache is not None:
                sqale_rating = float(sonar_cache.get("sqale_rating", 1.0))
                print(f"{repository.full_name}: {measure.name} is {sqale_rating} {measure.unit}")
                await self.cache_result(measure, repository, sqale_rating)
                return sqale_rating

            result = await asyncio.create_task(
                sonar.measure()
            )

            sqale_rating = float(result.get("sqale_rating", 1.0))
            print(f"{repository.full_name}: {measure.name} is {sqale_rating} {measure.unit}")
            await self.cache_result(measure, repository, sqale_rating)
            return sqale_rating
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
