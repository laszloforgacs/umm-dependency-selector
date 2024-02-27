import asyncio

from presentation.util.Subject import Subject
from presentation.viewpoint_list.input.ViewpointListInputState import ViewpointListInputState


class ViewpointListInputSubject(Subject):
    _state: ViewpointListInputState = ViewpointListInputState()
    _observers: set['Observer'] = set()

    @property
    def state(self) -> ViewpointListInputState:
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

    async def set_state(self, state: ViewpointListInputState):
        self._state = state
        await self.notify()