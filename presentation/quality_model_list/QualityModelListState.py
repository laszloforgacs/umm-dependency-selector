from dataclasses import dataclass
from typing import Optional

from presentation.util.ErrorState import ErrorState


@dataclass
class QualityModelListState:
    quality_model_list: list[str]
    is_loading: bool = False
    error: Optional[ErrorState] = None

    def copy(self, **kwargs):
        # Create a copy of the current instance with updated attributes
        return QualityModelListState(quality_models=kwargs.get('quality_model_list', self.quality_model_list),
                                     is_loading=kwargs.get('is_loading', self.is_loading),
                                     error=kwargs.get('error', self.error))
