from domain.model.Measure import BaseMeasure, MeasurementMethod


class SecurityRemediationEffort(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Security remediation effort", "effort unit", 1, MeasurementMethod.AUTOMATIC, visitor)
