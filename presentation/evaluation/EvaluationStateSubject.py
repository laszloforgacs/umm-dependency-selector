import asyncio

from presentation.evaluation.EvaluationScreenState import AHPReport
from presentation.util.Subject import Subject


class EvaluationStateSubject(Subject):
    _state: 'EvaluationState' = AHPReport(
        report={}
    )
    _observers: set['Observer'] = set()

    @property
    def state(self) -> 'EvaluationState':
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

    async def set_state(self, state: 'EvaluationState'):
        self._state = state
        await self.notify()
