from domain.model.MeasureableConcept import MeasurableConcept
from domain.model.SubCharacteristic import SubCharacteristic

"""
Comes from Sonar. Sonar collects relevant measures for maintainability mentioned in the literature under the term "Size". 
"""


class Size(SubCharacteristic[list[int]]):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Size", children)
