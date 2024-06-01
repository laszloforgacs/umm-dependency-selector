from domain.model.Measure import BaseMeasure, MeasurementMethod


class NumberOfStatements(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Number of statements", "statements", 1, MeasurementMethod.AUTOMATIC, visitor)

    def copy(self):
        return NumberOfStatements(
            visitor=self.visitor
        )