from abc import abstractmethod, ABC
from typing import Generic, TypeVar

from domain.model.ABCGenericMeta import ABCGenericMeta
from domain.model.Result import Result

T = TypeVar('T')


class SourceRepository(Generic[T], metaclass=ABCGenericMeta):
    @abstractmethod
    def __init__(self):
        pass

    async def fetch_repositories(self, urls: list[str]) -> Result[list[T]]:
        pass

    async def fetch_repository(self, url: str) -> Result[T]:
        pass

    def dispose(self):
        pass
