from presentation.core.QualityModelStateSubject import QualityModelStateSubject
from presentation.core.SharedViewModel import SharedViewModel
from presentation.quality_model_list.input.QualityModelUserInputState import QualityModelUserInputState
from presentation.quality_model_list.input.QualityModelUserInputSubject import QualityModelUserInputSubject


class QualityModelListViewModel:
    _quality_model_user_input_subject = QualityModelUserInputSubject()

    def __init__(self, shared_view_model: SharedViewModel):
        self._shared_view_model = shared_view_model

    @property
    def quality_model_state_subject(self) -> QualityModelStateSubject:
        return self._shared_view_model.quality_model_state_subject

    @property
    def quality_model_user_input_subject(self) -> QualityModelUserInputSubject:
        return self._quality_model_user_input_subject

    def wait_for_user_input(self):
        self._quality_model_user_input_subject.set_state(
            state=QualityModelUserInputState(
                should_wait_for_user_input=True
            )
        )

    def user_input_handled(self):
        self._quality_model_user_input_subject.set_state(
            state=QualityModelUserInputState(
                should_wait_for_user_input=False
            )
        )
