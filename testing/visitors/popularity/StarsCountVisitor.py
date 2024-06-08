from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor

"""
Measured in Augur. Called Star Count.
"""


class StarsCountVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            print(f"{repository.full_name}: {measure.name} is {repository.stargazers_count}")
            return repository.stargazers_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
