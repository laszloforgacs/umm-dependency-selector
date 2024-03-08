from presentation.core.Screen import Screen
from presentation.util.Observer import Observer


class EvaluationScreen(Screen, Observer):
    def __init__(self, navigator: 'Navigator', view_model: 'EvaluationViewModel'):
        self._navigator = navigator
        self._view_model = view_model

    async def on_created(self):
        self.observe_subjects()

    def on_destroy(self):
        self.dispose_observers()

    def observe_subjects(self):
        pass

    def dispose_observers(self):
        pass

    async def update(self, subject: 'EvaluationStateSubject'):
        pass
