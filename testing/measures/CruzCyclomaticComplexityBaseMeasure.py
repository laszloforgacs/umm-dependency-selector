from github.Repository import Repository

from domain.model.Measure import BaseMeasure


class CruzCyclomaticComplexityBaseMeasure(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Cruz Cyclomatic Complexity Base Measure", "", 1, visitor=visitor)

    def __copy__(self):
        return CruzCyclomaticComplexityBaseMeasure(
            visitor=self.visitor
        )
