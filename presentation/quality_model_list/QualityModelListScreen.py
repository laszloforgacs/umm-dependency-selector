import asyncio
from typing import Callable, Optional

import aioconsole

from domain.model.Result import Result, Success, Failure
from presentation.core.Screen import Screen
from presentation.quality_model_list.QualityModelListStateObserver import QualityModelListStateObserver
from presentation.quality_model_list.QualityModelListViewModel import QualityModelListViewModel
from presentation.quality_model_list.input.QualityModelUserInputObserver import QualityModelUserInputObserver


class QualityModelListScreen(Screen):
    _quality_model_list_state_observer: Optional[QualityModelListStateObserver] = None
    _quality_model_user_input_observer: Optional[QualityModelUserInputObserver] = None

    def __init__(self, view_model: QualityModelListViewModel, on_navigate_back: Callable[[None], None]):
        self._view_model = view_model
        self._on_navigate_back = on_navigate_back
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

    def on_created(self):
        self.observe_subjects()
        self._view_model.quality_model_state_subject.notify()
        self._view_model.quality_model_user_input_subject.notify()

    def on_destroy(self):
        self.dispose_observers()
        self._quality_model_list_state_observer = None
        self._quality_model_user_input_observer = None

    def _handle_update(self, should_wait_for_user_input: bool):
        if should_wait_for_user_input:
            self._view_model.wait_for_user_input()

    def _user_input_handled(self, is_handled: bool):
        if is_handled:
            self._view_model.user_input_handled()
