from abc import ABC, abstractmethod

from domain.model.QualityModel import QualityModel
from domain.model.Result import Result


class QualityModelRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    async def fetch_quality_models(self) -> Result[list[QualityModel]]:
        pass

    async def set_preference(
            self,
            filename: str,
            key: str,
            matrix_key: str,
            preference: str
    ):
        pass

    async def write_measurement_result_tree_to_json(self, quality_model: 'QualityModel', viewpoint: 'Viewpoint', repository_name: str):
        pass