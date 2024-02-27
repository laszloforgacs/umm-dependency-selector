from presentation.core.Screen import Screen
from presentation.viewpoint_list.ViewpointListViewModel import ViewpointListViewModel


class ViewpointListScreen(Screen):

    def __init__(self, navigator: 'Navigator', view_model: ViewpointListViewModel, selected_quality_model: str):
        self._navigator = navigator
        self._view_model = view_model
        self._selected_quality_model: str = selected_quality_model

    def on_created(self):
        viewpoints = self._view_model.viewpoints(selected_quality_model=self._selected_quality_model).keys()
        print(f"Viewpoints in VPLScreen on_created: {viewpoints}")

    def on_destroy(self):
        print("ViewpointListScreen destroyed")
