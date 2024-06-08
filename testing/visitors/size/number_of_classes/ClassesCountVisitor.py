import asyncio

from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.Sonar import Sonar

"""
Sonar measure
"""


class ClassesCountVisitor(BaseMeasureVisitor[int]):
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
                efficiency = self.efficiency(classes_count)
                print(f"{repository.full_name}: {measure.name} is {classes_count}, which is {efficiency} {measure.unit}")
                await self.cache_result(measure, repository, efficiency)
                return efficiency

            result = await asyncio.create_task(
                sonar.measure()
            )

            classes_count = int(result.get("classes", 0))
            efficiency = self.efficiency(classes_count)
            print(f"{repository.full_name}: {measure.name} is {classes_count}, which is {efficiency} {measure.unit}")
            await self.cache_result(measure, repository, efficiency)
            return efficiency
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def efficiency(self, measurement_value: int, optimal_value: int = 150, scaling_factor: float = 0.1) -> float:
        raw_efficiency = 100 - scaling_factor * (measurement_value - optimal_value) ** 2
        return max(0, raw_efficiency)
