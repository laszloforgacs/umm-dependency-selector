import asyncio

from presentation.core.QualityModelState import QualityModelState
from presentation.util.Subject import Subject


class QualityModelStateSubject(Subject):
    _state: QualityModelState = QualityModelState(
        quality_model_list=[]
    )
    _observers: set['Observer'] = set()

    @property
    def state(self) -> QualityModelState:
        return self._state

    def attach(self, observer: 'Observer'):
        self._observers.add(observer)

    def detach(self, observer: 'Observer'):
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self):
        tasks = []
        for observer in self._observers:
            tasks.append(asyncio.create_task(observer.update(self)))
        await asyncio.gather(*tasks)

    async def set_state(self, state: QualityModelState):
        self._state = state
        await self.notify()
