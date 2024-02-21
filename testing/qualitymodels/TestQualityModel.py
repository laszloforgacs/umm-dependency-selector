from domain.model.QualityModel import QualityModel
from domain.model.Viewpoint import Viewpoint


class TestQualityModel(QualityModel):
    def __init__(self, children: dict[str, Viewpoint] = {}):
        super().__init__("TestQualityModel", children)