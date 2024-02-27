from data.repository.QualityModelRepositoryImpl import QualityModelRepositoryImpl
from presentation.core.NavigationController import NavigationController
from presentation.core.Navigator import Navigator
from presentation.core.SharedViewModel import SharedViewModel
from presentation.quality_model_list.QualityModelListScreen import QualityModelListScreen
from presentation.quality_model_list.QualityModelListViewModel import QualityModelListViewModel
from presentation.viewpoint_list.ViewpointListScreen import ViewpointListScreen


class Dependencies:
    def __init__(self):
        self.navigation_controller = NavigationController()
        self.navigator = Navigator(
            navigation_controller=self.navigation_controller,
            dependencies=self
        )
        self.quality_model_repository = QualityModelRepositoryImpl()
        self.shared_view_model = SharedViewModel(
            quality_model_repository=self.quality_model_repository
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
            selected_quality_model=selected_quality_model
        )
