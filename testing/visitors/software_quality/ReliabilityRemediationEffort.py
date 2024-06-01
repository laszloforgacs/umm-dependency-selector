from domain.model.Measure import BaseMeasure, MeasurementMethod


class ReliabilityRemediationEffort(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Reliability remediation effort", "effort unit", 1, MeasurementMethod.AUTOMATIC, visitor)
