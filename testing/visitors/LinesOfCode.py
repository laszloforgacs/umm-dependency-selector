from domain.model.Measure import BaseMeasure, MeasurementMethod


class LinesOfCode(BaseMeasure[float]):
    def __init__(self, visitor=None):
        super().__init__("Lines of Code", "unit", 1.0, MeasurementMethod.AUTOMATIC, visitor)

    def copy(self):
        return LinesOfCode(
            visitor=self.visitor
        )
