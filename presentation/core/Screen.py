from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Generic

T = TypeVar('T')


class Screen(ABC, Generic[T]):
    @abstractmethod
    def __init__(self, on_navigate_back: Callable[[T], None]):
        pass

    @abstractmethod
    def on_created(self):
        pass

    @abstractmethod
    def on_destroy(self):
        pass
