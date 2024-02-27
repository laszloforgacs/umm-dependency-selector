import asyncio

from presentation.util.Subject import Subject
from presentation.viewpoint_list.ViewpointListScreenState import ViewpointListScreenState


class ViewpointListStateSubject(Subject):
    _state: ViewpointListScreenState = ViewpointListScreenState(viewpoints=[])
    _observers: list['Observer'] = []

    @property
    def state(self):
        return self._state

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    async def notify(self):
        tasks = []
        for observer in self._observers:
            tasks.append(asyncio.create_task(observer.update(self)))
        await asyncio.gather(*tasks)

    async def set_state(self, state: ViewpointListScreenState):
        self._state = state
        await self.notify()
