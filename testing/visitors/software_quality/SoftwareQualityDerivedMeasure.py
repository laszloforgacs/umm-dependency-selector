from domain.model.Measure import MeasurementMethod, DerivedMeasure

"""
Category 1 from SonarQube
"""
class SoftwareQualityDerivedMeasure(DerivedMeasure[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__("Software Quality", "unit", 1.0, MeasurementMethod.AUTOMATIC, children, normalize_visitor,
                         aggregate_visitor)
