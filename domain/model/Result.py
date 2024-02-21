from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional


T = TypeVar('T')

class Result(ABC, Generic[T]):
    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @property
    @abstractmethod
    def value(self) -> Optional[T]:
        pass


class Success(Result[T]):
    def __init__(self, value: T):
        self._value = value

    @property
    def is_valid(self) -> bool:
        return True

    @property
    def value(self) -> T:
        return self._value


class Failure(Result[Optional[T]]):
    def __init__(self, error_message: str, value: Optional[T] = None):
        self._error_message = error_message
        self._value = value

    @property
    def is_valid(self) -> bool:
        return False

    @property
    def value(self) -> Optional[T]:
        return self._value

    @property
    def message(self) -> str:
        return self._error_message
