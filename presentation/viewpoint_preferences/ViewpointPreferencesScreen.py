import aioconsole

from presentation.core.Screen import Screen
from presentation.util.Observer import Observer
from presentation.viewpoint_preferences.ViewpointPreferencesState import ViewpointState, UserInput, Loading, Error


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
            if viewpoint.is_valid_preference_matrix:
                print("Preference matrix is valid")
            else:
                await self.set_pref_or_go_back()
        elif isinstance(state, UserInput):
            print("User input state updated")
        elif isinstance(state, Loading):
            print("Loading...")
        elif isinstance(state, Error):
            print("Error: " + state.message)
        else:
            print("Unknown state")

    async def set_pref_or_go_back(self):
        while True:
            is_set_prefs = await aioconsole.ainput("Do you want to set preferences? (y/n): ")
            if is_set_prefs.lower() == "n":
                await self._navigator.navigate_up()
                break
            elif is_set_prefs.lower() == "y":
                print("Setting preferences...")
                break
            else:
                print("Invalid input, please try again")