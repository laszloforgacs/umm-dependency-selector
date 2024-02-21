from presentation.util.ErrorState import ErrorState
from presentation.util.Subject import Subject


class ErrorSubject(Subject):
    _state: ErrorState = None
    _observers: list['Observer'] = []

    def attach(self, observer: 'Observer') -> None:
        self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def set_state(self, state: ErrorState) -> None:
        self._state = state
        self.notify()