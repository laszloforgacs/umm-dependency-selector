import os

from github import Github
from github.Auth import Token

from data.repository.QualityModelRepositoryImpl import QualityModelRepositoryImpl
from data.repository.SourceRepositoryImpl import SourceRepositoryImpl
from presentation.core.navigation.NavigationController import NavigationController
from presentation.core.navigation.Navigator import Navigator
from presentation.core.SharedViewModel import SharedViewModel
from testing.visitors.VisitorFactory import MeasurableConceptVisitorFactory, DerivedMeasureVisitorFactory, \
    MeasureVisitorFactory
from presentation.evaluation.EvaluationScreen import EvaluationScreen
from presentation.evaluation.EvaluationViewModel import EvaluationViewModel
from presentation.quality_model_list.QualityModelListScreen import QualityModelListScreen
from presentation.quality_model_list.QualityModelListViewModel import QualityModelListViewModel
from presentation.viewpoint_list.ViewpointListScreen import ViewpointListScreen
from presentation.viewpoint_list.ViewpointListViewModel import ViewpointListViewModel
from presentation.viewpoint_preferences.ViewpointPreferencesScreen import ViewpointPreferencesScreen
from presentation.viewpoint_preferences.ViewpointPreferencesViewModel import ViewpointPreferencesViewModel
from util.GithubRateLimiter import GithubRateLimiter


class Dependencies:
    def __init__(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
        self.navigation_controller = NavigationController()
        self.base_measure_visitor_factory = MeasureVisitorFactory()
        self.derived_measure_visitor_factory = DerivedMeasureVisitorFactory()
        self.measurable_concept_visitor_factory = MeasurableConceptVisitorFactory()
        self.navigator = Navigator(
            navigation_controller=self.navigation_controller,
            dependencies=self
        )
        self.quality_model_repository = QualityModelRepositoryImpl(
            github_rate_limiter=self._github_rate_limiter,
            base_measure_visitor_factory=self.base_measure_visitor_factory,
            derived_measure_visitor_factory=self.derived_measure_visitor_factory,
            measurable_concept_visitor_factory=self.measurable_concept_visitor_factory
        )
        self.source_repository = SourceRepositoryImpl(
            github_rate_limiter=self._github_rate_limiter
        )
        self.shared_view_model = SharedViewModel(
            quality_model_repository=self.quality_model_repository,
            source_repository=self.source_repository
        )

    def provide_quality_model_list_screen(self):
        return lambda: QualityModelListScreen(
            navigator=self.navigator,
            view_model=QualityModelListViewModel(
                shared_view_model=self.shared_view_model
            )
        )

    def provide_viewpoint_list_screen(self, selected_quality_model: str):
        return lambda: ViewpointListScreen(
            navigator=self.navigator,
            view_model=ViewpointListViewModel(
                shared_view_model=self.shared_view_model
            ),
            selected_quality_model=selected_quality_model
        )

    def provide_viewpoint_preferences_screen(self, selected_quality_model: str, selected_viewpoint: str):
        return lambda: ViewpointPreferencesScreen(
            navigator=self.navigator,
            view_model=ViewpointPreferencesViewModel(
                shared_view_model=self.shared_view_model
            ),
            selected_quality_model=selected_quality_model,
            selected_viewpoint=selected_viewpoint
        )

    def provide_evaluation_screen(
            self,
            selected_quality_model: str,
            viewpoint: 'Viewpoint',
            characteristics: list['Characteristic'],
            repository_urls: list[str],
            comparisons: dict[str, 'Compare']
    ):
        return lambda: EvaluationScreen(
            navigator=self.navigator,
            view_model=EvaluationViewModel(
                shared_view_model=self.shared_view_model
            ),
            selected_quality_model=selected_quality_model,
            viewpoint=viewpoint,
            characteristics=characteristics,
            repository_urls=repository_urls,
            comparisons=comparisons
        )

    def dispose(self):
        self._github_rate_limiter.github_client.close()
