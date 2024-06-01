from domain.model.Measure import BaseMeasure, MeasurementMethod


class RepositoryAgeMeasure(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Repository Age", "year(s)", 1.0, MeasurementMethod.AUTOMATIC, visitor)
