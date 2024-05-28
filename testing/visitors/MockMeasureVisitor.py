from random import random

from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor


class MockMeasureVisitor(BaseMeasureVisitor[float]):
    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        random_top = random.uniform(10.0, 1000.0)
        rand = random.uniform(0.0, random_top)
        print(f"{repository.full_name}: {measure.name} is {rand}")
        return rand
