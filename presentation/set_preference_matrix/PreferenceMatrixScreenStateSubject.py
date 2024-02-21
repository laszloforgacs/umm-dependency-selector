from presentation.set_preference_matrix.PreferenceMatrixScreenState import PreferenceMatrixScreenState
from presentation.util.Subject import Subject


class PreferenceMatrixScreenStateSubject(Subject):
    _state: PreferenceMatrixScreenState = PreferenceMatrixScreenState(
        matrix={},
        preferences_shown_to_user=[],
        error=None
    )
    _observers: list['Observer'] = []

    @property
    def state(self) -> PreferenceMatrixScreenState:
        return self._state

    def attach(self, observer: 'Observer') -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def set_state(self, state: PreferenceMatrixScreenState) -> None:
        self._state = state
        self.notify()