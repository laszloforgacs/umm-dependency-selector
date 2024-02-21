from typing import Callable, Optional

from presentation.core.Screen import Screen
from presentation.quality_model_list.QualityModelListStateObserver import QualityModelListStateObserver
from presentation.quality_model_list.QualityModelListViewModel import QualityModelListViewModel


class QualityModelListScreen(Screen):
    _quality_model_list_state_observer: Optional[QualityModelListStateObserver] = None

    def __init__(self, view_model: QualityModelListViewModel, on_navigate_back: Callable[[None], None]):
        self._view_model = view_model
        self._on_navigate_back = on_navigate_back
        self._quality_model_list_state_observer = QualityModelListStateObserver()

    def observe_subjects(self):
        if self._quality_model_list_state_observer is not None:
            self._view_model.quality_model_state_subject.attach(self._quality_model_list_state_observer)

    def dispose_observers(self):
        if self._quality_model_list_state_observer is not None:
            self._view_model.quality_model_state_subject.detach(self._quality_model_list_state_observer)

    def on_created(self):
        self.observe_subjects()
        self._view_model.quality_model_state_subject.notify()

    def on_destroy(self):
        self.dispose_observers()
        self._quality_model_list_state_observer.dispose()
        self._quality_model_list_state_observer = None
