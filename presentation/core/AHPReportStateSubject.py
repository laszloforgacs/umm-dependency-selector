import asyncio

from presentation.core.AHPReportState import AHPReportState
from presentation.util.Subject import Subject


class AHPReportStateSubject(Subject):
    _state: AHPReportState = None
    _observers: set['Observer'] = set()

    @property
    def state(self) -> AHPReportState:
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

    async def set_state(self, state: AHPReportState):
        self._state = state
        await self.notify()