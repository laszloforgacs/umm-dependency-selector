from typing import Callable, Optional

from presentation.set_preference_matrix import PreferenceMatrixViewModel
from presentation.core.Screen import Screen
from presentation.set_preference_matrix.PreferenceMatrixScreenStateObserver import PreferenceMatrixScreenStateObserver


class PreferenceMatrixScreen(Screen):
    _preference_matrix_screen_state_observer: Optional[PreferenceMatrixScreenStateObserver] = None

    def __init__(self, view_model: PreferenceMatrixViewModel, on_navigate_back: Callable[[None], None]):
        self._view_model = view_model
        self._preference_matrix_screen_state_observer = PreferenceMatrixScreenStateObserver()
        self._on_navigate_back = on_navigate_back

    def observe_subjects(self):
        if self._preference_matrix_screen_state_observer is not None:
            self._view_model.preference_matrix_screen_state_subject.attach(
                self._preference_matrix_screen_state_observer)

    def dispose_observers(self):
        if self._preference_matrix_screen_state_observer is not None:
            self._view_model.preference_matrix_screen_state_subject.detach(
                self._preference_matrix_screen_state_observer)

    async def on_created(self):
        if len(self._view_model.preference_matrix_state.matrix) == 0:
            is_set_prefs = input("Do you want to set preferences? (y/n): ")
            if is_set_prefs.lower() == "n":
                return
            elif is_set_prefs.lower() == "y":
                self.observe_subjects()
                self._view_model.set_preference_matrix_state(self._view_model.preference_matrix_state.copy(
                    preferences_shown_to_user=self._view_model.preferences_shown
                ))

    async def on_destroy(self):
        self.dispose_observers()
        self._preference_matrix_screen_state_observer = None
