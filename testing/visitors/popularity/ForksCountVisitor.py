from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor

"""
Measured in Augur. Called Forks Count.
"""


class ForksCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            print(f"{repository.full_name}: {measure.name} is {repository.forks_count}")
            return repository.forks_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
