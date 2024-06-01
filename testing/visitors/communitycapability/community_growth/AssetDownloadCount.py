from domain.model.Measure import MeasurementMethod, BaseMeasure

"""
from CHAOSS. belongs to Comunity Growth, Number of Downloads
"""


class AssetDownloadCount(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__(
            "Count of asset downloads",
            "asset(s)",
            1.0,
            MeasurementMethod.AUTOMATIC,
            visitor
        )
