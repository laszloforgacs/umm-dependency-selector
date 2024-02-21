from dataclasses import dataclass
from typing import Optional

from domain.model.QualityModel import QualityModel
from presentation.util.ErrorState import ErrorState


@dataclass
class QualityModelState:
    quality_model_list: list[QualityModel]
    is_loading: bool = False
    error: Optional[ErrorState] = None

    def copy(self, **kwargs):
        return QualityModelState(quality_model_list=kwargs.get('quality_model_list', self.quality_model_list),
                                 is_loading=kwargs.get('is_loading', self.is_loading),
                                 error=kwargs.get('error', self.error))
