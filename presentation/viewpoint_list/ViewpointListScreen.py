from presentation.core.Screen import Screen


class ViewpointListScreen(Screen):
    def __init__(self, on_navigate_back):
        self._on_navigate_back = on_navigate_back

    def on_created(self):
        print("ViewpointListScreen created")

    def on_destroy(self):
        print("ViewpointListScreen destroyed")
