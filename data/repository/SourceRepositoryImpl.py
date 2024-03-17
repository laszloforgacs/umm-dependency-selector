import asyncio

from github import Github
from github.Auth import Token
from github.Repository import Repository

from domain.model.Result import Result, Success, Failure
from domain.repository.SourceRepository import SourceRepository


class SourceRepositoryImpl(SourceRepository[Repository]):
    def __init__(self, github_token: str):
        auth = Token(github_token)
        self._github = Github(auth=auth)

    async def fetch_repositories(self, urls: list[str]) -> Result[list[Repository]]:
        try:
            repo_full_names = [
                "/".join(url.split('/')[-2:])
                for url in urls
            ]

            repositories = [
                self._github.get_repo(url)
                for url in repo_full_names
            ]

            return Success(
                value=repositories
            )
        except Exception as e:
            return Failure(
                error_message=str(e)
            )

    async def fetch_repository(self, url: str) -> Result[Repository]:
        try:
            repo_full_name = "/".join(url.split('/')[-2:])
            repo = self._github.get_repo(repo_full_name)
            return Success(
                value=repo
            )
        except Exception as e:
            return Failure(
                error_message=str(e)
            )

    def dispose(self):
        self._github.close()
