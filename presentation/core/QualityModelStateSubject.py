import asyncio

from domain.model.Characteristic import Characteristic
from presentation.core.QualityModelState import QualityModelState
from presentation.util.Subject import Subject
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


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

    def set_preference(
            self,
            selected_quality_model: str,
            selected_viewpoint: str,
            component: 'CompositeComponent',
            pref_matrix: PrefMatrix
    ):
        if isinstance(component, Characteristic):
            for quality_model in self._state.quality_model_list:
                if quality_model.name == selected_quality_model:
                    quality_model.children.get(selected_viewpoint, {}).preference_matrix = pref_matrix
        else:
            for quality_model in self._state.quality_model_list:
                if quality_model.name == selected_quality_model:
                    quality_model.children.get(selected_viewpoint, {}).children.get(component.parent.name,
                                                                                    {}).preference_matrix = pref_matrix
