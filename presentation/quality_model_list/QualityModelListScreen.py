from typing import Optional

from presentation.core.navigation.Navigator import Navigator
from presentation.core.Screen import Screen
from presentation.quality_model_list.QualityModelListStateObserver import QualityModelListStateObserver
from presentation.quality_model_list.QualityModelListViewModel import QualityModelListViewModel
from presentation.quality_model_list.input.QualityModelUserInputObserver import QualityModelUserInputObserver
from presentation.util.Constants import VIEWPOINT_LIST_SCREEN


class QualityModelListScreen(Screen):
    _is_created: bool = False
    _quality_model_list_state_observer: QualityModelListStateObserver
    _quality_model_user_input_observer: QualityModelUserInputObserver

    def __init__(self, navigator: Navigator, view_model: QualityModelListViewModel):
        self._navigator = navigator
        self._view_model = view_model
        self._quality_model_list_state_observer = QualityModelListStateObserver(
            on_update=self._handle_update
        )
        self._quality_model_user_input_observer = QualityModelUserInputObserver(
            quality_model_list_state_subject=self._view_model.quality_model_state_subject,
            on_update=self._user_input_handled
        )

    def observe_subjects(self):
        self._view_model.quality_model_state_subject.attach(self._quality_model_list_state_observer)
        self._view_model.quality_model_user_input_subject.attach(self._quality_model_user_input_observer)

    def dispose_observers(self):
        self._view_model.quality_model_state_subject.detach(self._quality_model_list_state_observer)
        self._view_model.quality_model_user_input_subject.detach(self._quality_model_user_input_observer)

    async def on_created(self):
        self.observe_subjects()

        if self._is_created:
            await self._view_model.quality_model_state_subject.notify()

        if not self._is_created:
            self._is_created = True

    def on_destroy(self):
        self.dispose_observers()

    async def _handle_update(self, should_wait_for_user_input: bool):
        if should_wait_for_user_input:
            await self._view_model.wait_for_user_input()

    async def _user_input_handled(self, selected_quality_model: Optional[str]):
        if selected_quality_model is not None:
            await self._navigator.navigate_to(
                destination=VIEWPOINT_LIST_SCREEN,
                selected_quality_model=selected_quality_model
            )
            await self._view_model.user_input_handled()
