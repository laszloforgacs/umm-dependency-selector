import aioconsole
import validators

from presentation.core.AHPReportState import AHPReportState
from presentation.core.AHPReportStateSubject import AHPReportStateSubject
from presentation.core.Screen import Screen
from presentation.util.Constants import VIEWPOINT_PREFERENCES_EVALUATE_OR_RESET_INPUT, ERROR_INVALID_INPUT, \
    VIEWPOINT_WANT_TO_SET_PREFERENCES, EVALUATION_SCREEN, CONSISTENCY_RATIO_NOT_ACCEPTABLE
from presentation.util.Observer import Observer
from presentation.util.Util import print_items_with_last, print_ahp_ratings, accepted_ahp_values
from presentation.viewpoint_preferences.ComponentPreferencesState import ComponentsState, UrlInput, Loading, Error, \
    NavigateBack, SetPreferences, Refetch, SetOSSAspectPreferences
from presentation.viewpoint_preferences.ViewpointPreferencesStateSubject import ViewpointPreferencesStateSubject


class ViewpointPreferencesScreen(Screen, Observer):
    def __init__(self, navigator: 'Navigator', view_model: 'ViewpointPreferencesViewModel', selected_quality_model: str,
                 selected_viewpoint: str):
        self._navigator = navigator
        self._view_model = view_model
        self._selected_quality_model = selected_quality_model
        self._selected_viewpoint = selected_viewpoint

    async def on_created(self):
        self.observe_subjects()
        await self._view_model.fetch_viewpoint(
            selected_quality_model=self._selected_quality_model,
            selected_viewpoint=self._selected_viewpoint
        )

    def on_destroy(self):
        self.dispose_observers()

    def observe_subjects(self):
        self._view_model.pref_state_subject.attach(self)
        self._view_model.ahp_report_state_subject.attach(self)

    def dispose_observers(self):
        self._view_model.pref_state_subject.detach(self)
        self._view_model.ahp_report_state_subject.detach(self)

    async def update(self, subject: ViewpointPreferencesStateSubject | AHPReportStateSubject):
        state = subject.state
        if isinstance(state, ComponentsState):
            is_viewpoint_valid = state.viewpoint.is_valid_preference_matrix
            is_characteristics_valid = all(
                [
                    characteristic.is_valid_preference_matrix for characteristic in state.characteristics
                ]
            )
            is_all_valid = is_viewpoint_valid and is_characteristics_valid

            if is_all_valid:
                await self._view_model.create_ahp_hierarchy(
                    viewpoint=state.viewpoint,
                    characteristics=state.characteristics
                )
            else:
                await self.set_pref_or_go_back()

        elif isinstance(state, SetPreferences):
            preference_combination = state.preference_combination
            print(f"Setting preferences for {preference_combination[0].name} and {preference_combination[1].name}")
            print_ahp_ratings((preference_combination[0].name, preference_combination[1].name))
            preference_value = await self._handle_ahp_input()
            await self._view_model.set_preference(
                selected_quality_model=self._selected_quality_model,
                selected_viewpoint=self._selected_viewpoint,
                characteristic_tuple=preference_combination,
                preference=preference_value
            )

        elif isinstance(state, SetOSSAspectPreferences):
            preference_combination = state.oss_aspect_combination
            print(f"Setting preferences for {preference_combination[0]} and {preference_combination[1]} OSS Aspects")
            print_ahp_ratings((preference_combination[0], preference_combination[1]))
            preference_value = await self._handle_ahp_input()
            await self._view_model.set_oss_aspect_preference(
                selected_quality_model=self._selected_quality_model,
                selected_viewpoint=self._selected_viewpoint,
                oss_aspect_combination=preference_combination,
                preference=preference_value
            )

        elif isinstance(state, Refetch):
            await self._view_model.fetch_viewpoint(
                selected_quality_model=self._selected_quality_model,
                selected_viewpoint=self._selected_viewpoint
            )

        elif isinstance(state, UrlInput):
            while True:
                try:
                    url_input = await aioconsole.ainput("Enter a list of repository Urls separated by space: ")
                    urls = url_input.split(" ")
                    invalid_urls = []
                    for url in urls:
                        if not validators.url(url):
                            invalid_urls.append(url)
                    if len(invalid_urls) > 0:
                        print(f"Invalid urls: {invalid_urls}")
                        print("Please try again")
                    else:
                        await self._navigator.navigate_to(
                            destination=EVALUATION_SCREEN,
                            selected_quality_model=self._selected_quality_model,
                            viewpoint=state.viewpoint,
                            characteristics=state.characteristics,
                            repository_urls=urls
                        )
                        break
                except ValueError:
                    print(ERROR_INVALID_INPUT)
                    print("Please enter a valid value.")

        elif isinstance(state, AHPReportState):
            comparisons = state.comparisons
            under_consistency_threshold = [
                comparison for comparison in comparisons.values() if comparison.consistency_ratio > 0.1
            ]
            if len(under_consistency_threshold) > 0:
                for comparison in under_consistency_threshold:
                    print(f"Consistency Ratio for {comparison.name} is {comparison.consistency_ratio}.")
                print(CONSISTENCY_RATIO_NOT_ACCEPTABLE)
            await self.evaluate_reset_or_go_back(state)

        elif isinstance(state, Loading):
            print("Loading...")

        elif isinstance(state, Error):
            print("Error: " + state.message)

        elif isinstance(state, NavigateBack):
            await self._navigator.navigate_up()

        else:
            print("Unknown state")

    async def set_pref_or_go_back(self):
        while True:
            is_set_prefs = await aioconsole.ainput(VIEWPOINT_WANT_TO_SET_PREFERENCES)
            if is_set_prefs.lower() == "n":
                await self._view_model.pref_state_subject.set_state(NavigateBack())
                break
            elif is_set_prefs.lower() == "y":
                await self._view_model.prepare_preference_combinations()
                break
            else:
                print(ERROR_INVALID_INPUT)

    async def evaluate_reset_or_go_back(self, state: 'ComponentsState'):
        while True:
            items = [
                "Evaluate",
                "Reset preference matrix",
                "Go back"
            ]
            print(VIEWPOINT_PREFERENCES_EVALUATE_OR_RESET_INPUT)
            print_items_with_last(items)
            user_input = await aioconsole.ainput()
            if user_input == "1":
                await self._view_model.pref_state_subject.set_state(
                    state=UrlInput(
                        viewpoint=state.viewpoint,
                        characteristics=state.characteristics
                    )
                )
                break
            elif user_input == "2":
                await self._view_model.reset_preferences(
                    selected_quality_model=self._selected_quality_model,
                    selected_viewpoint=self._selected_viewpoint
                )
                break
            elif user_input == "3":
                await self._view_model.pref_state_subject.set_state(NavigateBack())
                break
            else:
                print(ERROR_INVALID_INPUT)

    async def _handle_ahp_input(self) -> str:
        while True:
            try:
                user_input = await aioconsole.ainput()
                input_value = user_input.replace(" ", "")
                if input_value in accepted_ahp_values():
                    return input_value
                else:
                    print(ERROR_INVALID_INPUT)
            except ValueError:
                print(ERROR_INVALID_INPUT)
                print("Please enter a valid value.")
                continue
