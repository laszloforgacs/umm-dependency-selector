from presentation.core.NavigationController import NavigationController
from presentation.util.Constants import QUALITY_MODEL_LIST_SCREEN, VIEWPOINT_LIST_SCREEN, VIEWPOINT_PREFERENCES_SCREEN, \
    EVALUATION_SCREEN


class Navigator:
    def __init__(self, navigation_controller: NavigationController, dependencies: 'Dependencies'):
        self._navigation_controller = navigation_controller
        self._dependencies = dependencies

    async def navigate_to(self, destination: str, **kwargs):
        if destination == QUALITY_MODEL_LIST_SCREEN:
            await self._navigation_controller.navigate_to(
                self._dependencies.provide_quality_model_list_screen()
            )

        if destination == VIEWPOINT_LIST_SCREEN:
            await self._navigation_controller.navigate_to(
                self._dependencies.provide_viewpoint_list_screen(
                    selected_quality_model=kwargs['selected_quality_model']
                )
            )

        if destination == VIEWPOINT_PREFERENCES_SCREEN:
            await self._navigation_controller.navigate_to(
                self._dependencies.provide_viewpoint_preferences_screen(
                    selected_quality_model=kwargs['selected_quality_model'],
                    selected_viewpoint=kwargs['selected_viewpoint']
                )
            )

        if destination == EVALUATION_SCREEN:
            await self._navigation_controller.navigate_to(
                self._dependencies.provide_evaluation_screen(
                    selected_quality_model=kwargs['selected_quality_model'],
                    viewpoint=kwargs['viewpoint'],
                    characteristics=kwargs['characteristics'],
                    repository_urls=kwargs['repository_urls'],
                    ahp_report=kwargs['ahp_report']
                )
            )

    async def navigate_up(self):
        await self._navigation_controller.navigate_back()
