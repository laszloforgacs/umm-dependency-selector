import asyncio

from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.Sonar import Sonar

"""
Sonar measure
"""


class SqaleIndexVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            sonar = Sonar(
                quality_model_name=measure.get_quality_model().name,
                viewpoint_name=measure.get_viewpoint().name,
                repository=repository
            )
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            sonar_cache = await sonar.get_cached_result()
            if sonar_cache is not None:
                sqale_index = int(sonar_cache.get("sqale_index", 0))
                print(f"{repository.full_name}: {measure.name} is {sqale_index} {measure.unit}")
                await self.cache_result(measure, repository, sqale_index)
                return sqale_index

            result = await asyncio.create_task(
                sonar.measure()
            )

            sqale_index = int(result.get("sqale_index", 0))
            print(f"{repository.full_name}: {measure.name} is {sqale_index} {measure.unit}")
            await self.cache_result(measure, repository, sqale_index)
            return sqale_index
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
