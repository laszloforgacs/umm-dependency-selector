from domain.model.Measure import BaseMeasure


class CruzNumberOfCommentsBaseMeasure(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Cruz Number of Comments Base Measure", "Line of comment", 5.0, visitor=visitor)

    def copy(self):
        return CruzNumberOfCommentsBaseMeasure(
            visitor=self.visitor
        )
