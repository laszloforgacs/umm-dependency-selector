import asyncio
from typing import Optional

from presentation.viewpoint_list.ViewpointListScreenState import ViewpointListScreenState
from presentation.viewpoint_list.ViewpointListStateSubject import ViewpointListStateSubject
from presentation.viewpoint_list.input.ViewpointListInputState import ViewpointListInputState
from presentation.viewpoint_list.input.ViewpointListInputSubject import ViewpointListInputSubject


class ViewpointListViewModel:
    _viewpoints_subject: ViewpointListStateSubject = ViewpointListStateSubject()
    _viewpoint_user_input_subject: ViewpointListInputSubject = ViewpointListInputSubject()

    def __init__(self, shared_view_model: 'SharedViewModel'):
        self._shared_view_model = shared_view_model

    @property
    def viewpoints_subject(self) -> ViewpointListStateSubject:
        return self._viewpoints_subject

    @property
    def viewpoint_input_subject(self) -> ViewpointListInputSubject:
        return self._viewpoint_user_input_subject

    async def fetch_viewpoints(self, selected_quality_model: str):
        viewpoints = self._shared_view_model.viewpoints(
            selected_quality_model=selected_quality_model
        )

        await self._viewpoints_subject.set_state(state=ViewpointListScreenState(viewpoints=viewpoints))

    async def wait_for_input(self):
        await self._viewpoint_user_input_subject.set_state(
            state=ViewpointListInputState(
                should_wait_for_input=True
            )
        )

    async def input_handled(self):
        await self._viewpoint_user_input_subject.set_state(
            state=ViewpointListInputState(
                should_wait_for_input=None
            )
        )
