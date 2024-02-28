import asyncio

from presentation.util.Subject import Subject
from presentation.viewpoint_preferences.ViewpointPreferencesState import ViewpointState


class ViewpointPreferencesStateSubject(Subject):
    _state: 'ViewpointPrefState' = ViewpointState(
        value=None
    )
    _observers: set['Observer'] = set()

    @property
    def state(self) -> 'ViewpointPrefState':
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

    async def set_state(self, state: 'ViewpointPrefState'):
        self._state = state
        await self.notify()
