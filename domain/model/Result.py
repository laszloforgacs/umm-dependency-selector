from abc import ABC, abstractmethod


class Result(ABC):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @property
    @abstractmethod
    def value(self) -> float | None:
        pass

    @property
    @abstractmethod
    def error(self) -> str | None:
        pass


class Success(Result):
    def __init__(self, value: float):
        self._value = value

    def is_valid(self) -> bool:
        return True

    def value(self) -> float:
        return self._value

    def error(self) -> str:
        return None


class Failure(Result):
    def __init__(self, error: str):
        self._error = error

    def is_valid(self) -> bool:
        return False

    def value(self) -> float:
        return None

    def error(self) -> str:
        return self._error
