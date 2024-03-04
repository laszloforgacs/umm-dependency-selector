import asyncio

from presentation.util.Subject import Subject
from presentation.viewpoint_preferences.ComponentPreferencesState import ComponentsState


class ViewpointPreferencesStateSubject(Subject):
    _state: 'ComponentPrefState' = ComponentsState(
        viewpoint=None,
        characteristics=[],
        sub_characteristics=[]
    )

    _observers: set['Observer'] = set()

    @property
    def state(self) -> 'ComponentPrefState':
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

    async def set_state(self, state: 'ComponentPrefState'):
        self._state = state
        await self.notify()
