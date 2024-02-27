from presentation.core.NavigationController import NavigationController
from presentation.util.Constants import QUALITY_MODEL_LIST_SCREEN, VIEWPOINT_LIST_SCREEN


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

    def navigate_up(self):
        self._navigation_controller.navigate_back()
