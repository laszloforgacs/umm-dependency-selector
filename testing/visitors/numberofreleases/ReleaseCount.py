from domain.model.Measure import BaseMeasure, MeasurementMethod


class ReleaseCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("ReleaseCount", "release", 1, MeasurementMethod.AUTOMATIC, visitor)

    def __copy__(self):
        return ReleaseCount(
            visitor=self.visitor
        )
