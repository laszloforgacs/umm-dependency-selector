import asyncio
import json

from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.Sonar import Sonar

"""
Sonar measure
"""


class DuplicatedBlocksCountVisitor(BaseMeasureVisitor[int]):
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
                duplicated_blocks = int(sonar_cache.get("duplicated_blocks", 0))
                print(f"{repository.full_name}: {measure.name} is {duplicated_blocks} {measure.unit}")
                await self.cache_result(measure, repository, duplicated_blocks)
                return duplicated_blocks

            result = await asyncio.create_task(
                sonar.measure()
            )

            duplicated_blocks = int(result.get("duplicated_blocks", 0))
            print(f"{repository.full_name}: {measure.name} is {duplicated_blocks} {measure.unit}")
            await self.cache_result(measure, repository, duplicated_blocks)
            return duplicated_blocks
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
