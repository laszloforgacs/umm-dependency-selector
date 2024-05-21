from domain.model.MeasureableConcept import MeasurableConcept
from domain.model.SubCharacteristic import SubCharacteristic


class EaseOfMaintenance(SubCharacteristic[list[int]]):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Ease of Maintenance", children)
