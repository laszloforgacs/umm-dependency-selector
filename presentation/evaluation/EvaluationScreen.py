import asyncio

from domain.model.Characteristic import Characteristic
from domain.model.Viewpoint import Viewpoint
from presentation.core.AHPReportState import AHPReportState
from presentation.core.AHPReportStateSubject import AHPReportStateSubject
from presentation.core.Screen import Screen
from presentation.evaluation.EvaluationScreenState import AHPReport, Loading, Error
from presentation.evaluation.EvaluationStateSubject import EvaluationStateSubject
from presentation.util.Observer import Observer


class EvaluationScreen(Screen, Observer):
    def __init__(
            self,
            navigator: 'Navigator',
            view_model: 'EvaluationViewModel',
            selected_quality_model: str,
            viewpoint: Viewpoint,
            characteristics: list[Characteristic],
            repository_urls: list[str]
    ):
        self._navigator = navigator
        self._view_model = view_model
        self._selected_quality_model = selected_quality_model
        self._viewpoint = viewpoint
        self._characteristics = characteristics
        self._repository_urls = repository_urls

    async def on_created(self):
        self.observe_subjects()
        await self._view_model.ahp_report_state_subject.notify()

    def on_destroy(self):
        self.dispose_observers()

    def observe_subjects(self):
        self._view_model.evaluation_state_subject.attach(self)
        self._view_model.ahp_report_state_subject.attach(self)

    def dispose_observers(self):
        self._view_model.evaluation_state_subject.detach(self)
        self._view_model.ahp_report_state_subject.detach(self)

    async def update(self, subject: EvaluationStateSubject | AHPReportStateSubject):
        state = subject.state
        if isinstance(state, AHPReportState):
            print(state.report)
        elif isinstance(state, AHPReport):
            print(state.report)
        elif isinstance(state, Loading):
            print("Loading...")
        elif isinstance(state, Error):
            print("Error: " + state.message)
        else:
            print("Unknown state")
