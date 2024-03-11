from domain.model.Measure import BaseMeasure, MeasurementMethod


class LinesOfCode(BaseMeasure[float]):
    def __init__(self):
        super().__init__("Lines of Code", "unit", 1.0, MeasurementMethod.AUTOMATIC)
