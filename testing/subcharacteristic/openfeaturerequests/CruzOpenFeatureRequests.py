from domain.model.MeasureableConcept import MeasurableConcept
from domain.model.SubCharacteristic import SubCharacteristic


class CruzOpenFeatureRequests(SubCharacteristic[list[int]]):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Currently open feature requests", children)