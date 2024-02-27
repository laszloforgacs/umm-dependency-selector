import asyncio

from presentation.quality_model_list.QualityModelListState import QualityModelListState
from presentation.util.Subject import Subject


class QualityModelListStateSubject(Subject):
    _state: QualityModelListState = QualityModelListState(
        quality_model_list=[],
        is_loading=False,
        error=None
    )
    _observers: set['Observer'] = set()

    @property
    def state(self) -> QualityModelListState:
        return self._state

    def attach(self, observer: 'Observer') -> None:
        self._observers.add(observer)

    def detach(self, observer: 'Observer') -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self) -> None:
        tasks = []
        for observer in self._observers:
            tasks.append(asyncio.create_task(observer.update(self)))
        await asyncio.gather(*tasks)

    async def set_state(self, state: QualityModelListState) -> None:
        self._state = state
        await self.notify()
