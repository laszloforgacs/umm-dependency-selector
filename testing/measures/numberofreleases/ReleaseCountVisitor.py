import os
from datetime import datetime, timedelta

from pydriller import Repository as PyDrillerRepository

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github.Repository import Repository as PyGithubRepository


class ReleaseCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: PyGithubRepository) -> int:
        try:
            base_path = os.getcwd()
            path_to_repository = f"{base_path}/{SOURCE_TEMP_DIR}/{repository.name}"
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            release_count = 0
            for tag in PyDrillerRepository(path_to_repository, only_releases=True, since=start_date, to=end_date).tags:
                release_count += 1

            print(f"{repository.full_name}: {measure.name} is {release_count}")
            return release_count
        except Exception as e:
            raise Exception(str(e))