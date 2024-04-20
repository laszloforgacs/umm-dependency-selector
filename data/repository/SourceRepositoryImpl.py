import asyncio
from pathlib import Path

from github.Repository import Repository

from git import Repo

from domain.model.Result import Result, Success, Failure
from domain.repository.SourceRepository import SourceRepository
from util.GithubRateLimiter import GithubRateLimiter

SOURCE_TEMP_DIR = "source_temp"


class SourceRepositoryImpl(SourceRepository[Repository]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter

    async def fetch_repositories(self, urls: list[str]) -> Result[list[Repository]]:
        try:
            repo_full_names = [
                "/".join(url.split('/')[-2:])
                for url in urls
            ]

            repositories = [
                self._github_rate_limiter.execute(
                    self._github_rate_limiter.github_client.get_repo,
                    url
                )
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
            repo = self._github_rate_limiter.execute(
                self._github_rate_limiter.github_client.get_repo,
                repo_full_name
            )
            return Success(
                value=repo
            )
        except Exception as e:
            return Failure(
                error_message=str(e)
            )

    async def clone_repositories(self, urls: list[str], destination: str = SOURCE_TEMP_DIR) -> Result[list[bool]]:
        try:
            results = []
            for url in urls:
                repo_name = url.split('/')[-1]
                if repo_name.endswith(".git"):
                    repo_name = repo_name[:-4]
                repo_path = f"{destination}/{repo_name}"

                if Path(repo_path).exists():
                    results.append(True)
                    print(f"{url} is already cloned")
                    continue

                repo = Repo.clone_from(url=url, to_path=repo_path)
                if repo:
                    results.append(True)
                    print(f"Cloned {url}")
                else:
                    results.append(False)
                    print(f"Failed to clone {url}")
            return Success(
                value=results
            )
        except Exception as e:
            print(str(e))
            return Failure(
                error_message=str(e)
            )

    async def dispose(self):
        await self._delete_temp_source_folders()

    async def _delete_temp_source_folders(self):
        process = await asyncio.create_subprocess_exec(
            "rm", "-rf", SOURCE_TEMP_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"Deleted {SOURCE_TEMP_DIR}")
        else:
            print(f"Failed to delete {SOURCE_TEMP_DIR}")
            print(stderr.decode().strip())
