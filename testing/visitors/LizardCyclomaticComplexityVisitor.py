from github.Repository import Repository

from domain.model.Result import Result
from presentation.core.visitors.Visitor import BaseMeasureVisitor


class LizardCyclomaticComplexityVisitor(BaseMeasureVisitor[Result[int]]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> Result[int]:
        pass
