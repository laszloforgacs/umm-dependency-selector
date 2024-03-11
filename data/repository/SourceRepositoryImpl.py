import asyncio

from domain.model.Result import Result, Success, Failure
from domain.repository.SourceRepository import SourceRepository


class SourceRepositoryImpl(SourceRepository):
    def __init__(self):
        pass

    async def fetch_repositories(self, urls: list[str]) -> Result[list[str]]:
        try:
            await asyncio.sleep(2)
            return Success(
                value=urls
            )
        except Exception as e:
            return Failure(
                error_message=str(e)
            )

    async def fetch_repository(self, url: str) -> str:
        return url
