import asyncio

from presentation.core.QualityModelState import QualityModelState
from presentation.util.Subject import Subject


class QualityModelStateSubject(Subject):
    _state: QualityModelState = QualityModelState(
        quality_model_list=[]
    )
    _observers: list['Observer'] = []

    @property
    def state(self) -> QualityModelState:
        return self._state

    def attach(self, observer: 'Observer'):
        self._observers.append(observer)

    def detach(self, observer: 'Observer'):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            asyncio.create_task(observer.update(self))

    def set_state(self, state: QualityModelState):
        self._state = state
        self.notify()