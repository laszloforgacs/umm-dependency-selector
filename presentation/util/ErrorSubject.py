from presentation.util.ErrorState import ErrorState
from presentation.util.Subject import Subject


class ErrorSubject(Subject):
    _state: ErrorState = None
    _observers: set['Observer'] = set()

    def attach(self, observer: 'Observer') -> None:
        self._observers.add(observer)

    def detach(self, observer: 'Observer') -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def set_state(self, state: ErrorState) -> None:
        self._state = state
        self.notify()