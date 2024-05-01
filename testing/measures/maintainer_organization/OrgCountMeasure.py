from domain.model.Measure import BaseMeasure, MeasurementMethod


class OrgCountMeasure(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Organization Count", "organization(s)", 1, MeasurementMethod.AUTOMATIC, visitor)