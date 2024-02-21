import itertools

from presentation.core.SharedViewModel import SharedViewModel
from presentation.set_preference_matrix.PreferenceMatrixScreenState import PreferenceMatrixScreenState
from presentation.set_preference_matrix.PreferenceMatrixScreenStateSubject import PreferenceMatrixScreenStateSubject


class PreferenceMatrixViewModel:
    _preference_matrix_screen_state_subject = PreferenceMatrixScreenStateSubject()

    def __init__(self, shared_view_model: SharedViewModel):
        available_quality_models = shared_view_model.quality_model_list
        selected_quality_model = available_quality_models[0]

        choice_of_viewpoints = list(selected_quality_model.children.keys())
        selected_viewpoint = choice_of_viewpoints[0]

        characteristics = list(selected_quality_model.children[selected_viewpoint].get_characteristics())
        print(characteristics)

        preferences_presented_to_user = list(itertools.combinations(characteristics, 2))
        self.preferences_shown = preferences_presented_to_user
        self._shared_view_model = shared_view_model

    @property
    def preference_matrix_screen_state_subject(self) -> PreferenceMatrixScreenStateSubject:
        return self._preference_matrix_screen_state_subject

    @property
    def preference_matrix_state(self) -> PreferenceMatrixScreenState:
        return self._preference_matrix_screen_state_subject.state

    def set_preference_matrix_state(self, new_state: PreferenceMatrixScreenState):
        self._preference_matrix_screen_state_subject.set_state(new_state)
