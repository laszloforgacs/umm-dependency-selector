import asyncio

from presentation.quality_model_list.input.QualityModelUserInputState import QualityModelUserInputState
from presentation.util.Subject import Subject


class QualityModelUserInputSubject(Subject):
    _state: QualityModelUserInputState = QualityModelUserInputState()
    _observers: set['Observer'] = set()

    @property
    def state(self) -> QualityModelUserInputState:
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

    async def set_state(self, state: QualityModelUserInputState):
        self._state = state
        await self.notify()
