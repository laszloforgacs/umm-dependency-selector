import itertools

from domain.model.Characteristic import Characteristic
from presentation.viewpoint_preferences.ComponentPreferencesState import Loading, ComponentsState, Error
from presentation.viewpoint_preferences.ViewpointPreferencesStateSubject import ViewpointPreferencesStateSubject


class ViewpointPreferencesViewModel:
    _pref_state_subject: 'ViewpointPreferencesStateSubject' = ViewpointPreferencesStateSubject()

    def __init__(self, shared_view_model: 'SharedViewModel'):
        self._shared_view_model = shared_view_model

    async def fetch_viewpoint(self, selected_quality_model: str, selected_viewpoint: str):
        await self._pref_state_subject.set_state(
            state=Loading()
        )

        try:
            viewpoint = self._shared_view_model.viewpoint(
                selected_quality_model=selected_quality_model,
                selected_viewpoint=selected_viewpoint
            )
            component_list = [
                [viewpoint],
                list(viewpoint.children.values())
            ]
            print(component_list)
            components = list(itertools.chain.from_iterable(component_list))
            print(components)
            await self._pref_state_subject.set_state(
                state=ComponentsState(
                    components=components
                )
            )
        except Exception as e:
            await self._pref_state_subject.set_state(
                state=Error(
                    message=str(e)
                )
            )

    async def set_preference(
            self,
            selected_quality_model: str,
            selected_viewpoint: str,
            component: 'CompositeComponent',
            characteristic_tuple: tuple[str, str],
            preference: str
    ):
        post_fix = f"-{component.name}" if isinstance(component, Characteristic) else ""
        filename = f"{selected_quality_model}-{selected_viewpoint}{post_fix}".replace(" ", "_")
        await self._shared_view_model.set_preference(
            filename=filename,
            component=component,
            characteristic_tuple=characteristic_tuple,
            preference=preference
        )


    @property
    def pref_state_subject(self) -> 'ViewpointPreferencesStateSubject':
        return self._pref_state_subject

    def characteristics(self, selected_quality_model: str, selected_viewpoint: str) -> dict[str, 'Characteristic']:
        return self._shared_view_model.characteristics(selected_quality_model, selected_viewpoint)
