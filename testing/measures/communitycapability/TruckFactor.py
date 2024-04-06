from domain.model.Measure import BaseMeasure


class TruckFactor(BaseMeasure[int]):
    def __init__(self, visitor=None):
        super().__init__("Truck factor", "developer", 1, visitor)