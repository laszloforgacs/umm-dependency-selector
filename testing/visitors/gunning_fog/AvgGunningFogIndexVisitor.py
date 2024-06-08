import os
from typing import Final

import aiofiles
from readability import Readability
from readability.exceptions import ReadabilityException

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from source_temp.PyGithub.github import Github
from source_temp.PyGithub.github.Repository import Repository
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Category 2 - belongs to Documentation
"""

SOURCE_TEMP_DIR: Final = "source_temp"


class AvgGunningFogIndexVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        super().__init__()

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            self._init()

            doc_texts = await self.get_documentation_files(repository)

            gunning_fog_indices = []
            for doc_text in doc_texts.values():
                try:
                    r = Readability(doc_text)
                    gunning_fog_index = r.gunning_fog()
                except ReadabilityException as e:
                    continue

                gunning_fog_indices.append(gunning_fog_index.score)

            if len(gunning_fog_indices) == 0.0:
                # 30.0 is the upper threshold for the Gunning Fog Index - arbitrary number
                # in the scource code, above 16.0 it is considered 'college level'
                # we return a high value because no documentation has Impact.NEGATIVE
                upper_threshold = 30.0
                print(f"{repository.full_name}: {measure.name} is {upper_threshold}")
                await self.cache_result(measure, repository, upper_threshold)
                return upper_threshold

            average_gunning_fog_index = sum(gunning_fog_indices) / len(gunning_fog_indices)
            print(f"{repository.full_name}: {measure.name} is {average_gunning_fog_index}")

            await self.cache_result(measure, repository, average_gunning_fog_index)
            return average_gunning_fog_index
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    async def get_documentation_files(self, repository: Repository) -> dict:
        doc_extensions = ['.md', '.rst', '.txt']
        doc_texts = {}

        local_repo_path = f"{SOURCE_TEMP_DIR}/{repository.name}"

        if not os.path.exists(local_repo_path):
            return {}

        contents = repository.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repository.get_contents(file_content.path))
            else:
                if any(file_content.name.endswith(ext) for ext in doc_extensions):
                    file_path = os.path.join(local_repo_path, file_content.path)
                    try:
                        async with aiofiles.open(file_path, "r") as file:
                            file_content = await file.read()
                            doc_texts[file_path] = file_content
                    except IOError as e:
                        print(f"Error reading file {file_path}: {e}")
                        return {}

        return doc_texts

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
