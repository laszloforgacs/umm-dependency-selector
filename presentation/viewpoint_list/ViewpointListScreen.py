import asyncio

import aioconsole

from domain.model.Result import Success
from presentation.core.Screen import Screen
from presentation.util.Constants import VIEWPOINT_LIST_INPUT, ERROR_INVALID_INPUT, VIEWPOINT_PREFERENCES_SCREEN
from presentation.util.Observer import Observer
from presentation.util.Util import print_items_with_last, handle_user_input
from presentation.viewpoint_list.ViewpointListScreenState import ViewpointListScreenState
from presentation.viewpoint_list.ViewpointListViewModel import ViewpointListViewModel
from presentation.viewpoint_list.input.ViewpointListInputState import ViewpointListInputState


class ViewpointListScreen(Screen, Observer):
    def __init__(self, navigator: 'Navigator', view_model: ViewpointListViewModel, selected_quality_model: str):
        self._navigator = navigator
        self._view_model = view_model
        self._selected_quality_model: str = selected_quality_model

    async def on_created(self):
        self.observe_subjects()
        await self._view_model.fetch_viewpoints(selected_quality_model=self._selected_quality_model)

    def observe_subjects(self):
        self._view_model.viewpoints_subject.attach(self)
        self._view_model.viewpoint_input_subject.attach(self)

    def dispose_observers(self):
        self._view_model.viewpoints_subject.detach(self)
        self._view_model.viewpoint_input_subject.detach(self)

    async def on_destroy(self):
        self.dispose_observers()

    async def update(self, subject: 'Subject') -> None:
        state = subject.state

        if isinstance(state, ViewpointListScreenState):
            viewpoints = subject.state.viewpoints
            print_items_with_last(viewpoints, "Go back")
            await self._view_model.wait_for_input()
        elif isinstance(state, ViewpointListInputState):
            if state.should_wait_for_input:
                while True:
                    user_input = await aioconsole.ainput(VIEWPOINT_LIST_INPUT)
                    viewpoint_dict = self._view_model.viewpoints_subject.state.viewpoints
                    dict_size = len(viewpoint_dict)
                    result = handle_user_input(
                        user_input=user_input,
                        list_size=dict_size,
                        error_message=ERROR_INVALID_INPUT
                    )

                    if isinstance(result, Success):
                        if result.value == dict_size + 1:
                            print("Going back...")
                            await self._view_model.input_handled()
                            await self._navigator.navigate_up()
                            break

                        viewpoint_list = list(viewpoint_dict.keys())
                        viewpoint = viewpoint_list[result.value - 1]
                        print("Selected Viewpoint: ", viewpoint)
                        await self._navigator.navigate_to(
                            destination=VIEWPOINT_PREFERENCES_SCREEN,
                            selected_quality_model=self._selected_quality_model,
                            selected_viewpoint=viewpoint
                        )
                        await self._view_model.input_handled()
                        break
                    else:
                        print(f"Error: {result.message}")
                        print("Please try again")
        else:
            raise ValueError(f"Unknown state: {state}")
