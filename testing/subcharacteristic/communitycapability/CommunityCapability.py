from domain.model.MeasureableConcept import MeasurableConcept
from domain.model.SubCharacteristic import SubCharacteristic

"""
First identified in Luoma
"""


class CommunityCapability(SubCharacteristic[list[int]]):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Community Capability", children)
