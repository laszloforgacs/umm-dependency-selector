from presentation.core.Screen import Screen


class ViewpointListScreen(Screen):

    def __init__(self, navigator: 'Navigator', selected_quality_model: str):
        self._navigator = navigator
        self._selected_quality_model: str = selected_quality_model
        print(f"Selected quality model in VPLScreen init: {self._selected_quality_model}")
        print("ViewpointListScreen init")

    def on_created(self):
        print("ViewpointListScreen created")

    def on_destroy(self):
        print("ViewpointListScreen destroyed")
