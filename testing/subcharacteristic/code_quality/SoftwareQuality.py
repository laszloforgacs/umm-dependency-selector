from domain.model.MeasureableConcept import MeasurableConcept
from domain.model.SubCharacteristic import SubCharacteristic


class SoftwareQuality(SubCharacteristic[list[float]]):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Software Quality", children)
