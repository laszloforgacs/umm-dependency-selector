from domain.model.Characteristic import Characteristic
from domain.model.Viewpoint import Viewpoint
from presentation.core.AHPReportState import AHPReportState
from presentation.core.AHPReportStateSubject import AHPReportStateSubject
from presentation.core.Screen import Screen
from presentation.core.SourceState import Loaded as RepositoryLoaded, Loading as RepositoryLoading, \
    Error as RepositoryError, CloningLoaded, CloningLoading, CloningError
from presentation.core.navigation.SourceStateSubject import SourceStateSubject
from presentation.evaluation.EvaluationScreenState import AHPReport, Loading as AHPReportLoading, \
    Error as AHPReportError, NavigateBack
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
            repository_urls: list[str],
            comparisons: dict[str, 'Compare']
    ):
        self._navigator = navigator
        self._view_model = view_model
        self._selected_quality_model = selected_quality_model
        self._viewpoint = viewpoint
        self._characteristics = characteristics
        self._repository_urls = repository_urls
        self._comparisons = comparisons

    async def on_created(self):
        self.observe_subjects()
        await self._view_model.fetch_repositories(self._repository_urls)

    async def on_destroy(self):
        self.dispose_observers()
        await self._view_model.dispose()

    def observe_subjects(self):
        self._view_model.evaluation_state_subject.attach(self)
        self._view_model.ahp_report_state_subject.attach(self)
        self._view_model.source_state_subject.attach(self)

    def dispose_observers(self):
        self._view_model.evaluation_state_subject.detach(self)
        self._view_model.ahp_report_state_subject.detach(self)
        self._view_model.source_state_subject.detach(self)

    async def update(self, subject: EvaluationStateSubject | AHPReportStateSubject | SourceStateSubject):
        state = subject.state
        if isinstance(state, RepositoryLoaded):
            await self._view_model.create_topsis_matrix(
                repositories=state.repositories,
                comparisons=self._comparisons,
                viewpoint=self._viewpoint,
                characteristics=self._characteristics
            )
        elif isinstance(state, RepositoryLoading):
            print("Fetching repository metadata... It might take a while.")
        elif isinstance(state, RepositoryError):
            print("Error fetching repositories: " + state.message)
        elif isinstance(state, CloningLoaded):
            print("Successfully cloned repositories.")
        elif isinstance(state, CloningLoading):
            print("Cloning repositories...")
        elif isinstance(state, CloningError):
            print("Error cloning repositories: " + state.message)
        elif isinstance(state, AHPReportState):
            print(state.report)
        elif isinstance(state, AHPReport):
            print(state.report)
        elif isinstance(state, AHPReportLoading):
            print("Loading...")
        elif isinstance(state, AHPReportError):
            print("Error: " + state.message)
        elif isinstance(state, NavigateBack):
            await self._navigator.navigate_up()
        else:
            print("Unknown state")
