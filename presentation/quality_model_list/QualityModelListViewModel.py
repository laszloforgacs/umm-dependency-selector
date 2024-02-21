from presentation.core.QualityModelStateSubject import QualityModelStateSubject
from presentation.core.SharedViewModel import SharedViewModel


class QualityModelListViewModel:
    def __init__(self, shared_view_model: SharedViewModel):
        self._shared_view_model = shared_view_model

    @property
    def quality_model_state_subject(self) -> QualityModelStateSubject:
        return self._shared_view_model.quality_model_state_subject
