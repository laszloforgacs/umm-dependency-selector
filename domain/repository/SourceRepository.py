from abc import abstractmethod, ABC

from domain.model.Result import Result


class SourceRepository(ABC):
    @abstractmethod
    def __init__(self):
        pass

    async def fetch_repositories(self, urls: list[str]) -> Result[list[str]]:
        pass

    async def fetch_repository(self, url: str) -> str:
        pass
