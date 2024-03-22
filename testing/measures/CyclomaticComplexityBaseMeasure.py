from github.Repository import Repository

from domain.model.Measure import BaseMeasure


class CyclomaticComplexityBaseMeasure(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Cyclomatic Complexity Base Measure", "", 1, visitor)

    def __copy__(self):
        return CyclomaticComplexityBaseMeasure(
            visitor=self.visitor
        )
