import itertools

from ahpy import ahpy

from domain.model.Characteristic import Characteristic
from domain.model.MeasureableConcept import OSSAspect
from domain.model.Viewpoint import Viewpoint
from presentation.core.AHPReportState import AHPReportState
from presentation.core.AHPReportStateSubject import AHPReportStateSubject
from presentation.util.Constants import PREFERENCES_NOT_ENOUGH_CHARACTERISTICS_OR_SUB_CHARACTERISTICS
from presentation.util.Util import convert_values_to_numerical
from presentation.viewpoint_preferences.ComponentPreferencesState import Loading, ComponentsState, Error, \
    SetPreferences, Refetch, SetOSSAspectPreferences
from presentation.viewpoint_preferences.ViewpointPreferencesStateSubject import ViewpointPreferencesStateSubject


class ViewpointPreferencesViewModel:
    _pref_state_subject: 'ViewpointPreferencesStateSubject' = ViewpointPreferencesStateSubject()
    _characteristics_preference_combinations: list[tuple['CompositeComponent', 'CompositeComponent']] = []
    _sub_characteristics_preference_combinations: list[tuple['CompositeComponent', 'CompositeComponent']] = []
    _oss_aspect_preference_combinations: list[OSSAspect] = []

    def __init__(self, shared_view_model: 'SharedViewModel'):
        self._shared_view_model = shared_view_model

    @property
    def pref_state_subject(self) -> 'ViewpointPreferencesStateSubject':
        return self._pref_state_subject

    @property
    def ahp_report_state_subject(self) -> AHPReportStateSubject:
        return self._shared_view_model.ahp_report_state_subject

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

            self._oss_aspect_preference_combinations = list(
                itertools.combinations(
                    [aspect.name for aspect in OSSAspect],
                    2
                )
            )

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
        elif len(self._oss_aspect_preference_combinations) > 0:
            await self._pref_state_subject.set_state(
                state=SetOSSAspectPreferences(
                    oss_aspect_combination=self._oss_aspect_preference_combinations.pop(0)
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
        filename = self._construct_file_name_for_components(
            selected_quality_model=selected_quality_model,
            selected_viewpoint=selected_viewpoint,
            characteristic_tuple=characteristic_tuple
        )
        await self._shared_view_model.set_preference(
            selected_quality_model=selected_quality_model,
            selected_viewpoint=selected_viewpoint,
            filename=filename,
            characteristic_tuple=characteristic_tuple,
            preference=preference
        )

        await self.prepare_preference_combinations()

    async def set_oss_aspect_preference(
            self,
            selected_quality_model: str,
            selected_viewpoint: str,
            oss_aspect_combination: tuple[OSSAspect, OSSAspect],
            preference: str
    ):
        filename = f"{selected_quality_model}-{selected_viewpoint}".replace(" ", "_")
        await self._shared_view_model.set_oss_aspect_preference(
            selected_quality_model=selected_quality_model,
            selected_viewpoint=selected_viewpoint,
            filename=filename,
            oss_aspect_combination=oss_aspect_combination,
            preference=preference
        )

        await self.prepare_preference_combinations()

    async def reset_preferences(
            self,
            selected_quality_model: str,
            selected_viewpoint: str
    ):
        try:
            viewpoint = self._shared_view_model.viewpoint(
                selected_quality_model=selected_quality_model,
                selected_viewpoint=selected_viewpoint
            )
            children = list(viewpoint.children.values())

            characteristics_preference_combinations = list(
                itertools.combinations(children, 2)
            )

            sub_characteristics_preference_combinations = list(itertools.chain.from_iterable([
                list(itertools.combinations(characteristic.children.values(), 2))
                for characteristic in viewpoint.children.values()
            ]))

            tasks = []
            for char_pref_combination in characteristics_preference_combinations:
                filename = self._construct_file_name_for_components(
                    selected_quality_model=selected_quality_model,
                    selected_viewpoint=selected_viewpoint,
                    characteristic_tuple=char_pref_combination
                )

                await self._shared_view_model.set_preference(
                    selected_quality_model=selected_quality_model,
                    selected_viewpoint=selected_viewpoint,
                    filename=filename,
                    characteristic_tuple=char_pref_combination,
                    preference=None
                )

            for sub_char_pref_combination in sub_characteristics_preference_combinations:
                filename = self._construct_file_name_for_components(
                    selected_quality_model=selected_quality_model,
                    selected_viewpoint=selected_viewpoint,
                    characteristic_tuple=sub_char_pref_combination
                )

                await self._shared_view_model.set_preference(
                    selected_quality_model=selected_quality_model,
                    selected_viewpoint=selected_viewpoint,
                    filename=filename,
                    characteristic_tuple=sub_char_pref_combination,
                    preference=None
                )

            await self._pref_state_subject.set_state(
                state=Refetch()
            )

        except Exception as e:
            await self._pref_state_subject.set_state(
                state=Error(
                    message=str(e)
                )
            )

    def characteristics(self, selected_quality_model: str, selected_viewpoint: str) -> dict[str, 'Characteristic']:
        return self._shared_view_model.characteristics(selected_quality_model, selected_viewpoint)

    async def create_ahp_hierarchy(self, viewpoint: Viewpoint, characteristics: list[Characteristic]):
        try:
            await self._pref_state_subject.set_state(
                state=Loading()
            )

            oss_aspects = [aspect.name for aspect in OSSAspect]
            all_comparisons = []

            viewpoint.preference_matrix = convert_values_to_numerical(viewpoint.preference_matrix)
            viewpoint.oss_aspect_preference_matrix = convert_values_to_numerical(viewpoint.oss_aspect_preference_matrix)

            for characteristic in characteristics:
                characteristic.preference_matrix = convert_values_to_numerical(characteristic.preference_matrix)

            characteristic_comparisons_by_oss_aspect = {}

            for aspect in oss_aspects:
                for characteristic in characteristics:
                    if aspect in characteristic.relevant_oss_aspects():
                        comparisons = characteristic_comparisons_by_oss_aspect.get(aspect, [])
                        comparison_names = [comparison.name for comparison in comparisons]
                        if characteristic.name not in comparison_names:
                            comparison = ahpy.Compare(
                                    name=characteristic.name,
                                    comparisons=characteristic.preference_matrix,
                                    precision=3
                                )
                            comparisons.append(comparison)
                            all_comparisons.append(comparison)
                            characteristic_comparisons_by_oss_aspect[aspect] = comparisons

            oss_aspect_comparisons = []
            for aspect, characteristic_comparisons in characteristic_comparisons_by_oss_aspect.items():
                comparison = ahpy.Compare(
                    name=aspect,
                    comparisons=viewpoint.preference_matrix,
                    precision=3
                )
                comparison.add_children(characteristic_comparisons)
                oss_aspect_comparisons.append(comparison)

            all_comparisons += oss_aspect_comparisons

            viewpoint_ahp_comparison = ahpy.Compare(
                name=viewpoint.name,
                comparisons=viewpoint.oss_aspect_preference_matrix,
                precision=3
            )
            all_comparisons.append(viewpoint_ahp_comparison)

            viewpoint_ahp_comparison.add_children(oss_aspect_comparisons)

            await self._shared_view_model.ahp_report_state_subject.set_state(
                state=AHPReportState(
                    comparisons={
                        comparison.name: comparison
                        for comparison in all_comparisons
                    },
                    viewpoint=viewpoint,
                    characteristics=characteristics
                )
            )

        except Exception as e:
            await  self._pref_state_subject.set_state(
                state=Error(
                    message=str(e)
                )
            )

    def _construct_file_name_for_components(
            self,
            selected_quality_model: str,
            selected_viewpoint: str,
            characteristic_tuple: tuple['CompositeComponent', 'CompositeComponent']
    ) -> str:
        parent = characteristic_tuple[0].parent
        post_fix = f"-{parent.name}" if isinstance(parent, Characteristic) else ""
        return f"{selected_quality_model}-{selected_viewpoint}{post_fix}".replace(" ", "_")
