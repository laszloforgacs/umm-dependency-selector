import itertools

from domain.model.Characteristic import Characteristic
from presentation.util.Constants import PREFERENCES_NOT_ENOUGH_CHARACTERISTICS_OR_SUB_CHARACTERISTICS
from presentation.viewpoint_preferences.ComponentPreferencesState import Loading, ComponentsState, Error, \
    SetPreferences, NavigateBack, Refetch
from presentation.viewpoint_preferences.ViewpointPreferencesStateSubject import ViewpointPreferencesStateSubject


class ViewpointPreferencesViewModel:
    _pref_state_subject: 'ViewpointPreferencesStateSubject' = ViewpointPreferencesStateSubject()
    _characteristics_preference_combinations: list[tuple['CompositeComponent', 'CompositeComponent']] = []
    _sub_characteristics_preference_combinations: list[tuple['CompositeComponent', 'CompositeComponent']] = []

    def __init__(self, shared_view_model: 'SharedViewModel'):
        self._shared_view_model = shared_view_model

    @property
    def pref_state_subject(self) -> 'ViewpointPreferencesStateSubject':
        return self._pref_state_subject

    @property
    def characteristics_preference_combinations(self) -> list[tuple[str, str]]:
        return self._characteristics_preference_combinations

    @property
    def sub_characteristics_preference_combinations(self) -> list[tuple[str, str]]:
        return self._sub_characteristics_preference_combinations

    async def fetch_viewpoint(self, selected_quality_model: str, selected_viewpoint: str):
        await self._pref_state_subject.set_state(
            state=Loading()
        )

        try:
            viewpoint = self._shared_view_model.viewpoint(
                selected_quality_model=selected_quality_model,
                selected_viewpoint=selected_viewpoint
            )
            children = list(viewpoint.children.values())
            grandchildren = [
                list(characteristic.children.values())
                for characteristic in viewpoint.children.values()
            ]

            self._characteristics_preference_combinations = list(
                itertools.combinations(children, 2)
            )
            self._sub_characteristics_preference_combinations = list(itertools.chain.from_iterable([
                list(itertools.combinations(characteristic.children.values(), 2))
                for characteristic in viewpoint.children.values()
            ]))
            await self._pref_state_subject.set_state(
                state=ComponentsState(
                    viewpoint=viewpoint,
                    characteristics=children,
                    sub_characteristics=list(itertools.chain.from_iterable(grandchildren))
                )
            )

        except Exception as e:
            await self._pref_state_subject.set_state(
                state=Error(
                    message=str(e)
                )
            )

    async def prepare_preference_combinations(self):
        await self._pref_state_subject.set_state(
            state=Loading()
        )

        if len(self._characteristics_preference_combinations) > 0:
            await self._pref_state_subject.set_state(
                state=SetPreferences(
                    preference_combination=self._characteristics_preference_combinations.pop(0)
                )
            )

        elif len(self._sub_characteristics_preference_combinations) > 0:
            await self._pref_state_subject.set_state(
                state=SetPreferences(
                    preference_combination=self._sub_characteristics_preference_combinations.pop(0)
                )
            )
        else:
            print(PREFERENCES_NOT_ENOUGH_CHARACTERISTICS_OR_SUB_CHARACTERISTICS)
            await self._pref_state_subject.set_state(
                state=Refetch()
            )

    async def set_preference(
            self,
            selected_quality_model: str,
            selected_viewpoint: str,
            characteristic_tuple: tuple['CompositeComponent', 'CompositeComponent'],
            preference: str
    ):
        parent = characteristic_tuple[0].parent
        post_fix = f"-{parent.name}" if isinstance(parent, Characteristic) else ""
        filename = f"{selected_quality_model}-{selected_viewpoint}{post_fix}".replace(" ", "_")
        new_pref_matrix = await self._shared_view_model.set_preference(
            selected_quality_model=selected_quality_model,
            selected_viewpoint=selected_viewpoint,
            filename=filename,
            characteristic_tuple=characteristic_tuple,
            preference=preference
        )

        #self._pref_state_subject.set_preference(
        #    component=characteristic_tuple[0],
        #    pref_matrix=new_pref_matrix
        #)

        await self.prepare_preference_combinations()

    def characteristics(self, selected_quality_model: str, selected_viewpoint: str) -> dict[str, 'Characteristic']:
        return self._shared_view_model.characteristics(selected_quality_model, selected_viewpoint)
