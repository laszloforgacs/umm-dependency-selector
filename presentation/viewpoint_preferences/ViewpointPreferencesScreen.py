import aioconsole

from presentation.core.Screen import Screen
from presentation.util.Constants import VIEWPOINT_PREFERENCES_EVALUATE_OR_RESET_INPUT, ERROR_INVALID_INPUT, \
    VIEWPOINT_WANT_TO_SET_PREFERENCES
from presentation.util.Observer import Observer
from presentation.util.Util import print_items_with_last
from presentation.viewpoint_preferences.ViewpointPreferencesState import ViewpointState, UserInput, Loading, Error, \
    NavigateBack


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

    def dispose_observers(self):
        self._view_model.pref_state_subject.detach(self)

    async def update(self, subject: 'ViewpointPrefState'):
        state = subject.state
        if isinstance(state, ViewpointState):
            viewpoint = state.value
            #if viewpoint.is_valid_preference_matrix:
            print("Preference matrix is valid")
            await self.evaluate_reset_or_go_back()
            #else:
             #   await self.set_pref_or_go_back()
        elif isinstance(state, UserInput):
            print("User input state updated")
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
                print("Setting preferences...")
                break
            else:
                print(ERROR_INVALID_INPUT)

    async def evaluate_reset_or_go_back(self):
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
                print("Evaluating...")
                break
            elif user_input == "2":
                print("Resetting pref matrix...")
                break
            elif user_input == "3":
                await self._view_model.pref_state_subject.set_state(NavigateBack())
                break
            else:
                print(ERROR_INVALID_INPUT)