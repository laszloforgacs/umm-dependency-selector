import asyncio

from presentation.quality_model_list.QualityModelListState import QualityModelListState
from presentation.util.Subject import Subject


class QualityModelListStateSubject(Subject):
    _state: QualityModelListState = QualityModelListState(
        quality_model_list=[],
        is_loading=False,
        error=None
    )
    _observers: list['Observer'] = []

    @property
    def state(self) -> QualityModelListState:
        return self._state

    def attach(self, observer: 'Observer') -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def set_state(self, state: QualityModelListState) -> None:
        self._state = state
        self.notify()
