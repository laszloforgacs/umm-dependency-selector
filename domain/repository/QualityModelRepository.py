from abc import ABC, abstractmethod

from domain.model.QualityModel import QualityModel
from domain.model.Result import Result


class QualityModelRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    async def fetch_quality_models(self) -> Result[list[QualityModel]]:
        pass
