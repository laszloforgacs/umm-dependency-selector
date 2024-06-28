import asyncio

from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.Sonar import Sonar

"""
Sonar measure
"""


class NumberOfClassesVisitor(BaseMeasureVisitor[int]):
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
                classes_count = int(sonar_cache.get("classes", 0))
                print(f"{repository.full_name}: {measure.name} is {classes_count}")
                await self.cache_result(measure, repository, classes_count)
                return classes_count

            result = await asyncio.create_task(
                sonar.measure()
            )

            classes_count = int(result.get("classes", 0))
            print(f"{repository.full_name}: {measure.name} is {classes_count}")
            await self.cache_result(measure, repository, classes_count)
            return classes_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
